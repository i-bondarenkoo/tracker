const API_URL = 'http://127.0.0.1:8000'

async function loginRequest(email, password) {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        body: formData,
    });
    if (!response.ok){
        throw new Error('Неверный логин или пароль');
    }
    return await response.json();
}

async function registerRequest(userData) {
    const response = await fetch(`${API_URL}/auth/register`,{
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(userData),
    });
    if (!response.ok) {
        throw new Error('Ошибка регистрации');
    }
    return await response.json();
}

async function getTransactions(token) {
    const response = await fetch(`${API_URL}/transaction/?start=0&stop=1000`, {
        headers: {'Authorization': `Bearer ${token}`},

    });
    if (!response.ok) {
        throw new Error('Не удалось загрузить транзакции');
    }
    return await response.json()
}
async function loadCategoriesIntoSelect() {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_URL}/category/?start=0&stop=100`, {
        headers: { 'Authorization': `Bearer ${token}` },
    });
    const categories = await response.json();

    const select = document.getElementById('transaction-category-id');
    select.innerHTML = '<option value="">Выберите категорию</option>';

    categories.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat.id;
        option.textContent = cat.name;
        select.appendChild(option);
    });
}