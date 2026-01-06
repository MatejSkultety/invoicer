import { mount } from '@vue/test-utils'
import { expect, test } from 'vitest'
import CatalogItemModal from '../src/modules/catalog_items/CatalogItemModal.vue'

test('shows validation errors for empty fields', async () => {
  const wrapper = mount(CatalogItemModal, {
    props: {
      modelValue: true
    }
  })

  await wrapper.find('form').trigger('submit')

  expect(wrapper.text()).toContain('Name is required')
  expect(wrapper.text()).toContain('Description is required')
  expect(wrapper.text()).toContain('Unit is required')
  expect(wrapper.text()).toContain('Price is required')
})

test('emits trimmed payload on submit', async () => {
  const wrapper = mount(CatalogItemModal, {
    props: {
      modelValue: true
    }
  })

  await wrapper.find('input[name="name"]').setValue('  Design work  ')
  await wrapper.find('textarea[name="description"]').setValue('  Product design  ')
  await wrapper.find('input[name="unit"]').setValue('  hour  ')
  await wrapper.find('input[name="unit_price"]').setValue(' 7,5 ')
  await wrapper.find('input[name="tax_rate"]').setValue(' 21% ')

  await wrapper.find('form').trigger('submit')

  const emitted = wrapper.emitted('submit')
  expect(emitted).toBeTruthy()
  expect(emitted[0][0]).toEqual({
    name: 'Design work',
    description: 'Product design',
    unit: 'hour',
    unit_price: 750,
    tax_rate: 21
  })
})

test('shows validation errors for max length', async () => {
  const wrapper = mount(CatalogItemModal, {
    props: {
      modelValue: true
    }
  })

  await wrapper.find('input[name="name"]').setValue('Design work')
  await wrapper.find('textarea[name="description"]').setValue('a'.repeat(1025))
  await wrapper.find('input[name="unit"]').setValue('hour')
  await wrapper.find('input[name="unit_price"]').setValue('12.00')

  await wrapper.find('form').trigger('submit')

  expect(wrapper.text()).toContain('Description must be at most 1024 characters')
})

test('prefills edit form and emits updated payload', async () => {
  const wrapper = mount(CatalogItemModal, {
    props: {
      modelValue: false,
      item: {
        id: 'item-1',
        name: 'Design work',
        description: 'Product design services',
        unit: 'hour',
        unit_price: 15000,
        tax_rate: 21
      }
    }
  })

  await wrapper.setProps({ modelValue: true })

  expect(wrapper.find('h2').text()).toBe('Edit catalog item')
  expect(wrapper.find('input[name="name"]').element.value).toBe('Design work')
  expect(wrapper.find('textarea[name="description"]').element.value).toBe('Product design services')
  expect(wrapper.find('input[name="unit"]').element.value).toBe('hour')
  expect(wrapper.find('input[name="unit_price"]').element.value).toBe('150.00')
  expect(wrapper.find('input[name="tax_rate"]').element.value).toBe('21')

  await wrapper.find('input[name="unit_price"]').setValue('200.50')
  await wrapper.find('input[name="tax_rate"]').setValue('10%')
  await wrapper.find('form').trigger('submit')

  const emitted = wrapper.emitted('submit')
  expect(emitted).toBeTruthy()
  expect(emitted[0][0]).toEqual({
    name: 'Design work',
    description: 'Product design services',
    unit: 'hour',
    unit_price: 20050,
    tax_rate: 10
  })
})
