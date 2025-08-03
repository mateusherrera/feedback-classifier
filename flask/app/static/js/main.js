document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault()
    const username = document.getElementById('username').value
    const password = document.getElementById('password').value

    const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })

    const data = await res.json()
    if (res.ok) {
        localStorage.setItem('access', data.access)
        localStorage.setItem('refresh', data.refresh)
        window.location.href = '/dashboard'
    } else {
        alert(data.details || 'Erro ao logar')
    }
})
