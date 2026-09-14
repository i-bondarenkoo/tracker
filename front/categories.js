let allCategories = [];

async function loadCategoriesIntoSelect() {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_URL}/category/?start=0&stop=100`, {
        headers: { 'Authorization': `Bearer ${token}` },
    });
    const categories = await response.json();
    allCategories = categories;

    const select = document.getElementById('transaction-category-id');
    select.innerHTML = '<option value="">Выберите категорию</option>';
    categories.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat.id;
        option.textContent = cat.name;
        select.appendChild(option);
    });
}

function getCategoryName(id) {
    const found = allCategories.find(c => c.id === id);
    return found ? found.name : `Категория #${id}`;
}