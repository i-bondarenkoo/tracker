document.getElementById('categorySubmit').addEventListener('click', async () => {
    const token = localStorage.getItem('token');
    const categoryData = {
        name: document.getElementById('category-name').value,
    };

    const response = await fetch(`${API_URL}/category/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify(categoryData),
    });

    if (!response.ok) {
        const errorData = await response.json();
        alert(errorData.detail || 'Ошибка при создании категории');
        return;
    }
    document.getElementById('categoryModal').style.display = 'none';
    alert('Категория создана');
});