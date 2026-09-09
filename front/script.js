document.querySelector('.btn-enter').addEventListener('click', () => {
    document.getElementById('loginModal').style.display = 'flex';
});

document.getElementById('loginClose').addEventListener('click', () => {
    document.getElementById('loginModal').style.display = 'none';
});

document.querySelector('.btn-register').addEventListener('click', ()=> {
    document.getElementById('registerModal').style.display = 'flex';
});

document.getElementById('registerClose').addEventListener('click', ()=> {
    document.getElementById('registerModal').style.display = 'none';
});

document.addEventListener('DOMContentLoaded', () => {
    loadAndRenderTransactions();
});
document.querySelector('.filter-date-btn').addEventListener('click', () => {
    document.getElementById('filter-rangeModal').style.display = 'flex';
});
document.getElementById('filterClose').addEventListener('click', ()=> {
    document.getElementById('filter-rangeModal').style.display = 'none';
});

document.querySelector('.add-category-btn').addEventListener('click', () => {
    document.getElementById('categoryModal').style.display = 'flex';
});
document.getElementById('categoryClose').addEventListener('click', ()=> {
    document.getElementById('categoryModal').style.display = 'none';
});
document.querySelector('.add-transaction-btn').addEventListener('click', async () => {
    await loadCategoriesIntoSelect();
    document.getElementById('transactionModal').style.display = 'flex';
});
document.getElementById('transactionClose').addEventListener('click', ()=> {
    document.getElementById('transactionModal').style.display = 'none';
});

document.getElementById('transactionSubmit').addEventListener('click', async () => {
    const token = localStorage.getItem('token');
    const transactionData = {
        description: document.getElementById('transaction-description').value,
        amount: Number(document.getElementById('transaction-amount').value),
        cost: Number(document.getElementById('transaction-cost').value),
        category_id: Number(document.getElementById('transaction-category-id').value),
        transaction_date: document.getElementById('transaction-transaction-date').value,
    };

    const response = await fetch(`${API_URL}/transaction/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(transactionData),
    });

    if (!response.ok) {
        const errorData = await response.json();
        alert(errorData.detail || 'Ошибка при создании траты');
        return;
    }

    document.getElementById('transactionModal').style.display = 'none';
    loadAndRenderTransactions();
});

document.getElementById('filterSubmit').addEventListener('click', async () => {
    const token = localStorage.getItem('token');
    const dateFrom = document.getElementById('date-from').value;
    const dateTo = document.getElementById('date-to').value;

    let url = `${API_URL}/transaction/?start=0&stop=1000`;
    if (dateFrom) url += `&date_from=${dateFrom}`;
    if (dateTo) url += `&date_to=${dateTo}`;

    const response = await fetch(url, {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${token}` },
    });

    if (!response.ok) {
        const errorData = await response.json();
        alert(errorData.detail || 'Ошибка при фильтрации');
        return;
    }
    const transactions = await response.json();
    document.getElementById('filter-rangeModal').style.display = 'none';
    renderTransactions(transactions);
});


document.getElementById('categorySubmit').addEventListener('click', async () => {
    const token = localStorage.getItem('token');
    const categoryData = {
        name: document.getElementById('category-name').value,

    };

    const response = await fetch(`${API_URL}/category/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
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

async function loadAndRenderTransactions() {
    const token = localStorage.getItem('token');
    if (!token) return ;
    let transactions;
    try {
        transactions = await getTransactions(token);
    } catch (err) {
        console.error(err.message);
        return ;
    }
    renderTransactions(transactions);
}

function renderTransactions(transactions) {
    const container = document.getElementById('transactionsContainer');
    container.innerHTML = '';

    const grouped = groupByDate(transactions);

    for (const date in grouped) {
        const card = document.createElement('div');
        card.className = 'day-card';

        let rowsHtml = '';
        for (const t of grouped[date]) {
            rowsHtml += `
                <div class="expense-row">
                    <span>${t.description}</span>
                    <div class="expense-right">
                        <span>${t.cost} ₽</span>
                        <div class="expense-actions">
                            <button class="icon-btn" onclick="editTransaction(${t.id})">✎</button>
                            <button class="icon-btn" onclick="deleteTransactionHandler(${t.id})">✕</button>
                        </div>
                    </div>
                </div>
`;
        }
        card.innerHTML = `
            <div class="card-inside">
                <h3>${date}</h3>
                ${rowsHtml}
            </div>
        `;
        container.appendChild(card);
    }
}

function groupByDate(transactions) {
    const grouped = {};
    for (const t of transactions) {
        const date = t.transaction_date;
        if (!grouped[date]) {
            grouped[date] = [];
        }
        grouped[date].push(t);
    }
    return grouped;
}