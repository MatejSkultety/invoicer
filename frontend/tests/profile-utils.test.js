import { describe, expect, test, vi } from 'vitest'
import {
  clearProfileStatusCache,
  emptyProfile,
  getCachedProfileStatus,
  isProfileComplete,
  normalizeProfile,
  refreshProfileStatus,
  setProfileStatusCache
} from '../src/modules/users/profile'

const getCurrentUser = vi.hoisted(() => vi.fn())

vi.mock('../src/modules/users/api', () => ({
  getCurrentUser
}))

describe('profile helpers', () => {
  test('empty profile is not complete', () => {
    expect(isProfileComplete(emptyProfile())).toBe(false)
  })

  test('complete profile passes the check', () => {
    const profile = {
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

    expect(isProfileComplete(profile)).toBe(true)
  })

  test('normalize profile fills missing fields', () => {
    const normalized = normalizeProfile({ name: 'Acme Co' })
    expect(normalized.name).toBe('Acme Co')
    expect(normalized.email).toBe('')
  })

  test('profile status cache can be reset', () => {
    setProfileStatusCache(true)
    expect(getCachedProfileStatus()).toBe(true)
    clearProfileStatusCache()
    expect(getCachedProfileStatus()).toBe(null)
  })

  test('refreshProfileStatus sets cache and returns the value', async () => {
    clearProfileStatusCache()
    getCurrentUser.mockResolvedValue({
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
    })

    const result = await refreshProfileStatus()

    expect(result).toBe(true)
    expect(getCachedProfileStatus()).toBe(true)
  })

  test('refreshProfileStatus resets cache on failure', async () => {
    clearProfileStatusCache()
    getCurrentUser.mockRejectedValue(new Error('fail'))

    const result = await refreshProfileStatus()

    expect(result).toBe(null)
    expect(getCachedProfileStatus()).toBe(null)
  })
})
