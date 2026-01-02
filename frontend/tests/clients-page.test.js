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
      id: 1,
      name: 'Acme Co',
      email: 'hello@acme.test',
      address: '123 Main St',
      notes: 'Priority account'
    }
  ])

  const wrapper = mount(ClientsPage)
  await flushPromises()

  expect(wrapper.text()).toContain('Acme Co')
  expect(wrapper.text()).toContain('hello@acme.test')
})

test('create flow calls the API and shows a toast', async () => {
  const payload = {
    name: 'Nova Labs',
    address: '88 Market St',
    email: 'team@nova.test',
    notes: 'Pilot customer'
  }

  listClients.mockResolvedValueOnce([]).mockResolvedValueOnce([{
    id: 2,
    ...payload
  }])
  createClient.mockResolvedValue({ id: 2, ...payload })

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
