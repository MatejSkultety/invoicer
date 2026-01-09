import { getCurrentUser } from './api'

export const REQUIRED_FIELDS = [
  'name',
  'address',
  'city',
  'country',
  'trade_licensing_office',
  'ico',
  'dic',
  'email',
  'phone',
  'bank',
  'iban',
  'swift'
]

export function emptyProfile() {
  return REQUIRED_FIELDS.reduce((profile, field) => {
    profile[field] = ''
    return profile
  }, {})
}

export function normalizeProfile(profile) {
  const normalized = emptyProfile()
  REQUIRED_FIELDS.forEach((field) => {
    const value = profile?.[field]
    normalized[field] = typeof value === 'string' ? value : ''
  })
  return normalized
}

export function isProfileComplete(profile) {
  return REQUIRED_FIELDS.every((field) => {
    const value = profile?.[field]
    return typeof value === 'string' && value.trim().length > 0
  })
}

export async function hasCompleteProfile() {
  try {
    const profile = await getCurrentUser()
    return isProfileComplete(profile)
  } catch (error) {
    return false
  }
}
