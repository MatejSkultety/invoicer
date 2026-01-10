const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    },
    ...options
  })

  if (!response.ok) {
    let detail = 'Request failed'
    try {
      const data = await response.json()
      if (data && typeof data.detail === 'string') {
        detail = data.detail
      }
    } catch (error) {
      // ignore JSON parsing errors
    }
    const error = new Error(detail)
    error.status = response.status
    throw error
  }

  if (response.status === 204) {
    return null
  }

  return response.json()
}

export async function getCurrentUser() {
  return request('/api/users/me')
}

export async function updateCurrentUser(payload) {
  return request('/api/users/me', {
    method: 'PUT',
    body: JSON.stringify(payload)
  })
}
