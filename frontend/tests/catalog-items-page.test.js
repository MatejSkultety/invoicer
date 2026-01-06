import { flushPromises, mount } from '@vue/test-utils'
import { beforeEach, expect, test, vi } from 'vitest'
import CatalogItemModal from '../src/modules/catalog_items/CatalogItemModal.vue'
import CatalogItemsPage from '../src/modules/catalog_items/CatalogItemsPage.vue'
import {
  archiveCatalogItem,
  createCatalogItem,
  listCatalogItems,
  updateCatalogItem
} from '../src/modules/catalog_items/api'

const addToast = vi.hoisted(() => vi.fn())

vi.mock('../src/modules/catalog_items/api', () => ({
  listCatalogItems: vi.fn(),
  createCatalogItem: vi.fn(),
  updateCatalogItem: vi.fn(),
  archiveCatalogItem: vi.fn()
}))

vi.mock('../src/shared/toast', () => ({
  useToast: () => ({
    addToast
  })
}))

beforeEach(() => {
  addToast.mockClear()
  listCatalogItems.mockReset()
  createCatalogItem.mockReset()
  updateCatalogItem.mockReset()
  archiveCatalogItem.mockReset()
})

test('renders catalog items from the API', async () => {
  listCatalogItems.mockResolvedValue([
    {
      id: 'f2a1c8a0-1234-4c66-9a12-123456789abc',
      name: 'Design work',
      description: 'Product design services',
      unit: 'hour',
      unit_price: 15000,
      tax_rate: 21
    }
  ])

  const wrapper = mount(CatalogItemsPage)
  await flushPromises()

  expect(wrapper.text()).toContain('Design work')
  expect(wrapper.text()).toContain('150.00 / hour')
  expect(wrapper.text()).toContain('Product design services')
  expect(wrapper.text()).toContain('Tax 21%')
})

test('create flow calls the API and shows a toast', async () => {
  const payload = {
    name: 'QA session',
    description: 'Testing services',
    unit: 'hour',
    unit_price: 9000,
    tax_rate: 21
  }

  listCatalogItems.mockResolvedValueOnce([]).mockResolvedValueOnce([
    {
      id: 'a5f6c8d1-5678-4b21-8b33-abcdef123456',
      ...payload
    }
  ])
  createCatalogItem.mockResolvedValue({
    id: 'a5f6c8d1-5678-4b21-8b33-abcdef123456',
    ...payload
  })

  const wrapper = mount(CatalogItemsPage)
  await flushPromises()

  await wrapper.find('button.primary').trigger('click')
  const modal = wrapper.findComponent(CatalogItemModal)
  modal.vm.$emit('submit', payload)

  await flushPromises()

  expect(createCatalogItem).toHaveBeenCalledWith(payload)
  expect(addToast).toHaveBeenCalledWith('Catalog item created')
})

test('shows an error state when loading fails', async () => {
  listCatalogItems.mockRejectedValue(new Error('Network error'))

  const wrapper = mount(CatalogItemsPage)
  await flushPromises()

  expect(wrapper.text()).toContain('Network error')
})
