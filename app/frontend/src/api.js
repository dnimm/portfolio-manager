export async function apiRequest(path, method = 'GET', body = null) {
  const token = localStorage.getItem('token')

  const options = {
    method: method,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
  }

  if (body) {
    options.body = JSON.stringify(body)
  }

  const response = await fetch(path, options)
  const data = await response.json().catch(() => null)

  if (!response.ok) {
    throw new Error(data?.detail || data?.error || 'Request failed')
  }

  return data
}