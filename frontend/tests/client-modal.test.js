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
  expect(wrapper.text()).toContain('Email is required')
  expect(wrapper.text()).toContain('Notes are required')
})

test('emits trimmed payload on submit', async () => {
  const wrapper = mount(ClientModal, {
    props: {
      modelValue: true
    }
  })

  const inputs = wrapper.findAll('input')
  await inputs[0].setValue('  Acme  ')
  await inputs[1].setValue('  123 Main  ')
  await inputs[2].setValue('  hello@acme.test  ')
  await wrapper.find('textarea').setValue('  Notes here  ')

  await wrapper.find('form').trigger('submit')

  const emitted = wrapper.emitted('submit')
  expect(emitted).toBeTruthy()
  expect(emitted[0][0]).toEqual({
    name: 'Acme',
    address: '123 Main',
    email: 'hello@acme.test',
    notes: 'Notes here'
  })
})
