export function startLogin() {
  window.location.href = 'http://127.0.0.1:5000/users/login'
}

export async function exchangeCodeForToken(code) {
  localStorage.setItem('token', code)
  return code
}

export function getToken() {
  return localStorage.getItem('token')
}

export function logout() {
  localStorage.removeItem('token')
}

export function getUsername() {
  const token = getToken()

  if (!token) {
    return ''
  }

  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.username || payload['cognito:username'] || payload.sub || ''
  } catch {
    return ''
  }
}