document.querySelector('.stats-btn').addEventListener('click', () => {
    document.getElementById('statsModal').style.display = 'flex';
});
document.getElementById('statsClose').addEventListener('click', () => {
    document.getElementById('statsModal').style.display = 'none';
});

document.getElementById('statsSubmit').addEventListener('click', async () => {
    const token = localStorage.getItem('token');
    const dateFrom = document.getElementById('stats-date-from').value;
    const dateTo = document.getElementById('stats-date-to').value;

    if (!dateFrom || !dateTo) {
        alert('Укажите обе даты');
        return;
    }

    const params = `date_from=${dateFrom}&date_to=${dateTo}`;

    try {
        const [byCategory, topCategories, aboveAverage] = await Promise.all([
            fetch(`${API_URL}/users/me/spending-by-category?${params}`, {
                headers: { 'Authorization': `Bearer ${token}` },
            }).then(r => r.json()),
            fetch(`${API_URL}/users/me/spending-top-categories?${params}&limit=3`, {
                headers: { 'Authorization': `Bearer ${token}` },
            }).then(r => r.json()),
            fetch(`${API_URL}/users/me/transactions-average-value?${params}`, {
                headers: { 'Authorization': `Bearer ${token}` },
            }).then(r => r.json()),
        ]);

        renderStats(byCategory, topCategories, aboveAverage);
    } catch (err) {
        alert('Ошибка при загрузке статистики');
    }
});

function renderStats(byCategory, topCategories, aboveAverage) {
    const container = document.getElementById('statsResults');

    let html = '<h4>Расходы по категориям</h4><ul>';
    byCategory.forEach(c => {
        html += `<li>${getCategoryName(c.category_id)}: ${c.total_amount_by_category} ₽</li>`;
    });
    html += '</ul>';

    html += '<h4>Топ категорий</h4><ul>';
    topCategories.forEach(c => {
        html += `<li>${c.name}: ${c.total_amount_by_category} ₽</li>`;
    });
    html += '</ul>';

    html += '<h4>Траты выше среднего чека</h4><ul>';
    aboveAverage.forEach(t => {
        html += `<li>${t.description}: ${t.amount * t.cost} ₽</li>`;
    });
    html += '</ul>';

    container.innerHTML = html;
}