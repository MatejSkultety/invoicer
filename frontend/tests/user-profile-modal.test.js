import { mount } from '@vue/test-utils'
import { expect, test } from 'vitest'
import UserProfileModal from '../src/modules/users/UserProfileModal.vue'

const baseProfile = {
  name: 'Acme Co',
  address: '123 Main St',
  city: 'Prague',
  country: 'Czechia',
  trade_licensing_office: 'Prague 1',
  ico: '12345678',
  dic: 'CZ12345678',
  email: 'billing@acme.test',
  phone: '+420123456789',
  bank: 'Example Bank',
  iban: 'CZ6508000000192000145399',
  swift: 'GIBACZPX'
}

test('shows validation errors for empty required fields', async () => {
  const wrapper = mount(UserProfileModal, {
    props: {
      modelValue: true,
      profile: baseProfile
    }
  })

  await wrapper.find('input[name="name"]').setValue('')
  await wrapper.find('input[name="address"]').setValue('')
  await wrapper.find('input[name="city"]').setValue('')
  await wrapper.find('input[name="country"]').setValue('')
  await wrapper.find('input[name="trade_licensing_office"]').setValue('')
  await wrapper.find('input[name="ico"]').setValue('')
  await wrapper.find('input[name="dic"]').setValue('')
  await wrapper.find('input[name="email"]').setValue('')
  await wrapper.find('input[name="phone"]').setValue('')
  await wrapper.find('input[name="bank"]').setValue('')
  await wrapper.find('input[name="iban"]').setValue('')
  await wrapper.find('input[name="swift"]').setValue('')

  await wrapper.find('form').trigger('submit')

  expect(wrapper.text()).toContain('Name is required')
  expect(wrapper.text()).toContain('Address is required')
  expect(wrapper.text()).toContain('City is required')
  expect(wrapper.text()).toContain('Country is required')
  expect(wrapper.text()).toContain('Trade licensing office is required')
  expect(wrapper.text()).toContain('IČO is required')
  expect(wrapper.text()).toContain('DIČ is required')
  expect(wrapper.text()).toContain('Email is required')
  expect(wrapper.text()).toContain('Phone is required')
  expect(wrapper.text()).toContain('Bank is required')
  expect(wrapper.text()).toContain('IBAN is required')
  expect(wrapper.text()).toContain('SWIFT is required')
})

test('emits trimmed payload', async () => {
  const wrapper = mount(UserProfileModal, {
    props: {
      modelValue: true,
      profile: baseProfile
    }
  })

  await wrapper.find('input[name="name"]').setValue('  Acme Updated  ')
  await wrapper.find('input[name="address"]').setValue('  456 Market St  ')
  await wrapper.find('input[name="city"]').setValue('  Brno  ')
  await wrapper.find('input[name="country"]').setValue('  Czechia  ')
  await wrapper.find('input[name="trade_licensing_office"]').setValue('  Prague 2  ')
  await wrapper.find('input[name="ico"]').setValue('  12345678  ')
  await wrapper.find('input[name="dic"]').setValue('  CZ12345678  ')
  await wrapper.find('input[name="email"]').setValue('  billing@acme.test  ')
  await wrapper.find('input[name="phone"]').setValue('  +420123456789  ')
  await wrapper.find('input[name="bank"]').setValue('  Example Bank  ')
  await wrapper.find('input[name="iban"]').setValue('  CZ6508000000192000145399  ')
  await wrapper.find('input[name="swift"]').setValue('  GIBACZPX  ')

  await wrapper.find('form').trigger('submit')

  const emitted = wrapper.emitted('submit')
  expect(emitted).toBeTruthy()
  expect(emitted[0][0]).toEqual({
    name: 'Acme Updated',
    address: '456 Market St',
    city: 'Brno',
    country: 'Czechia',
    trade_licensing_office: 'Prague 2',
    ico: '12345678',
    dic: 'CZ12345678',
    email: 'billing@acme.test',
    phone: '+420123456789',
    bank: 'Example Bank',
    iban: 'CZ6508000000192000145399',
    swift: 'GIBACZPX'
  })
})
