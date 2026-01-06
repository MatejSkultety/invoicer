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

export async function listCatalogItems() {
  return request('/api/catalog-items')
}

export async function createCatalogItem(payload) {
  return request('/api/catalog-items', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

export async function updateCatalogItem(id, payload) {
  return request(`/api/catalog-items/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload)
  })
}

export async function archiveCatalogItem(id) {
  return request(`/api/catalog-items/${id}`, {
    method: 'DELETE'
  })
}
