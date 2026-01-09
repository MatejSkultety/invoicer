import { describe, expect, test } from 'vitest'
import { emptyProfile, isProfileComplete, normalizeProfile } from '../src/modules/users/profile'

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
})
