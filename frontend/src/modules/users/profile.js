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

let cachedComplete = null

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

export function getCachedProfileStatus() {
  return cachedComplete
}

export function clearProfileStatusCache() {
  cachedComplete = null
}

export function setProfileStatusCache(value) {
  cachedComplete = value
}

export async function refreshProfileStatus() {
  try {
    const profile = await getCurrentUser()
    cachedComplete = isProfileComplete(profile)
  } catch (error) {
    cachedComplete = null
  }
  return cachedComplete
}

export async function hasCompleteProfile() {
  if (cachedComplete !== null) {
    return cachedComplete
  }

  return refreshProfileStatus()
}
