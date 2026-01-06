import { flushPromises, mount } from '@vue/test-utils'
import { beforeEach, expect, test, vi } from 'vitest'
import ClientModal from '../src/modules/clients/ClientModal.vue'
import ClientsPage from '../src/modules/clients/ClientsPage.vue'
import { archiveClient, createClient, listClients, updateClient } from '../src/modules/clients/api'

const addToast = vi.hoisted(() => vi.fn())

vi.mock('../src/modules/clients/api', () => ({
  listClients: vi.fn(),
  createClient: vi.fn(),
  updateClient: vi.fn(),
  archiveClient: vi.fn()
}))

vi.mock('../src/shared/toast', () => ({
  useToast: () => ({
    addToast
  })
}))

beforeEach(() => {
  addToast.mockClear()
  listClients.mockReset()
  createClient.mockReset()
  updateClient.mockReset()
  archiveClient.mockReset()
})

test('renders clients from the API', async () => {
  listClients.mockResolvedValue([
    {
      id: 'b7c1c8a0-1234-4c66-9a12-123456789abc',
      name: 'Acme Co',
      address: '123 Main St',
      city: 'Prague',
      country: 'Czechia',
      main_contact_method: 'email',
      main_contact: 'hello@acme.test',
      additional_contact: null,
      ico: null,
      dic: null,
      notes: 'Priority account',
      favourite: true
    }
  ])

  const wrapper = mount(ClientsPage)
  await flushPromises()

  expect(wrapper.text()).toContain('Acme Co')
  expect(wrapper.text()).toContain('📧 Email: hello@acme.test')
  expect(wrapper.text()).toContain('⭐ Favourite')
})

test('create flow calls the API and shows a toast', async () => {
  const payload = {
    name: 'Nova Labs',
    address: '88 Market St',
    city: 'Brno',
    country: 'Czechia',
    main_contact_method: 'discord',
    main_contact: 'nova-team',
    additional_contact: '',
    ico: '',
    dic: '',
    notes: 'Pilot customer',
    favourite: false
  }

  listClients.mockResolvedValueOnce([]).mockResolvedValueOnce([{
    id: 'a5f6c8d1-5678-4b21-8b33-abcdef123456',
    ...payload
  }])
  createClient.mockResolvedValue({
    id: 'a5f6c8d1-5678-4b21-8b33-abcdef123456',
    ...payload
  })

  const wrapper = mount(ClientsPage)
  await flushPromises()

  await wrapper.find('button.primary').trigger('click')
  const modal = wrapper.findComponent(ClientModal)
  modal.vm.$emit('submit', payload)

  await flushPromises()

  expect(createClient).toHaveBeenCalledWith(payload)
  expect(addToast).toHaveBeenCalledWith('Client created')
})

test('shows an error state when loading fails', async () => {
  listClients.mockRejectedValue(new Error('Network error'))

  const wrapper = mount(ClientsPage)
  await flushPromises()

  expect(wrapper.text()).toContain('Network error')
})
