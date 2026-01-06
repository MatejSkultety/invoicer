import { mount } from '@vue/test-utils'
import { expect, test } from 'vitest'
import ClientModal from '../src/modules/clients/ClientModal.vue'

test('shows validation errors for empty fields', async () => {
  const wrapper = mount(ClientModal, {
    props: {
      modelValue: true
    }
  })

  await wrapper.find('form').trigger('submit')

  expect(wrapper.text()).toContain('Name is required')
  expect(wrapper.text()).toContain('Address is required')
  expect(wrapper.text()).toContain('City is required')
  expect(wrapper.text()).toContain('Country is required')
  expect(wrapper.text()).toContain('Main contact is required')
})

test('emits trimmed payload on submit', async () => {
  const wrapper = mount(ClientModal, {
    props: {
      modelValue: true
    }
  })

  await wrapper.find('input[name="name"]').setValue('  Acme  ')
  await wrapper.find('input[name="address"]').setValue('  123 Main  ')
  await wrapper.find('input[name="city"]').setValue('  Prague  ')
  await wrapper.find('input[name="country"]').setValue('  Czechia  ')
  await wrapper.find('select[name="main_contact_method"]').setValue('email')
  await wrapper.find('input[name="main_contact"]').setValue('  hello@acme.test  ')
  await wrapper.find('input[name="additional_contact"]').setValue('  backup  ')
  await wrapper.find('input[name="ico"]').setValue('  12345678  ')
  await wrapper.find('input[name="dic"]').setValue('  CZ12345678  ')
  await wrapper.find('textarea[name="notes"]').setValue('  Notes here  ')

  await wrapper.find('form').trigger('submit')

  const emitted = wrapper.emitted('submit')
  expect(emitted).toBeTruthy()
  expect(emitted[0][0]).toEqual({
    name: 'Acme',
    address: '123 Main',
    city: 'Prague',
    country: 'Czechia',
    main_contact_method: 'email',
    main_contact: 'hello@acme.test',
    additional_contact: 'backup',
    ico: '12345678',
    dic: 'CZ12345678',
    notes: 'Notes here',
    favourite: false
  })
})

test('shows validation errors for max length', async () => {
  const wrapper = mount(ClientModal, {
    props: {
      modelValue: true
    }
  })

  await wrapper.find('input[name="name"]').setValue('a'.repeat(257))
  await wrapper.find('input[name="address"]').setValue('123 Main')
  await wrapper.find('input[name="city"]').setValue('Prague')
  await wrapper.find('input[name="country"]').setValue('Czechia')
  await wrapper.find('select[name="main_contact_method"]').setValue('email')
  await wrapper.find('input[name="main_contact"]').setValue('hello@acme.test')

  await wrapper.find('form').trigger('submit')

  expect(wrapper.text()).toContain('Name must be at most 256 characters')
})
