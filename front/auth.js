document.getElementById('loginSubmit').addEventListener('click', async () => {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
        const data = await loginRequest(email, password);
        localStorage.setItem('token', data.access_token);
        document.getElementById('loginModal').style.display = 'none';
        await loadCategoriesIntoSelect();
        loadAndRenderTransactions();
        alert('Вход выполнен!');
    } catch (err) {
        alert(err.message);
    }
});

document.getElementById('registerSubmit').addEventListener('click', async () => {
    const userData = {
        first_name: document.getElementById('register-first_name').value,
        last_name: document.getElementById('register-last_name').value,
        email: document.getElementById('register-email').value,
        password: document.getElementById('register-password').value,
    };

    try {
        await registerRequest(userData);
        document.getElementById('registerModal').style.display = 'none';
        alert('Регистрация успешна! Теперь войдите.');
    } catch (err) {
        alert(err.message);
    }
});