let currentTransactions = [];

async function loadAndRenderTransactions() {
    const token = localStorage.getItem('token');
    if (!token) return;
    await loadCategoriesIntoSelect();
    let transactions;
    try {
        transactions = await getTransactions(token);
    } catch (err) {
        console.error(err.message);
        return;
    }
    currentTransactions = transactions;
    renderTransactions(transactions);
}

function renderTransactions(transactions) {
    const container = document.getElementById('transactionsContainer');
    container.innerHTML = '';
    const grouped = groupByDate(transactions);

    for (const date in grouped) {
        const card = document.createElement('div');
        card.className = 'day-card';

        let dayTotal = 0;
        let rowsHtml = '';

        for (const t of grouped[date]) {
            const rowSum = t.amount * t.cost;
            dayTotal += rowSum;

            rowsHtml += `
                <tr>
                    <td>${t.description}</td>
                    <td>${t.amount}</td>
                    <td>${t.cost} ₽</td>
                    <td>${rowSum} ₽</td>
                    <td>
                        <div class="actions-cell">
                            <button class="icon-btn" onclick="editTransaction(${t.id})">✎</button>
                            <button class="icon-btn" onclick="deleteTransactionHandler(${t.id})">✕</button>
                        </div>
                    </td>
                </tr>
            `;
        }

        card.innerHTML = `
            <div class="card-inside">
                <h3>${date}</h3>
                <table class="expense-table">
                    <thead>
                        <tr>
                            <th>Описание</th>
                            <th>Кол-во</th>
                            <th>Цена</th>
                            <th>Сумма</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>${rowsHtml}</tbody>
                </table>
                <div class="day-total">Итого за день: ${dayTotal} ₽</div>
            </div>
        `;
        container.appendChild(card);
    }
}

function groupByDate(transactions) {
    const grouped = {};
    for (const t of transactions) {
        const date = t.transaction_date;
        if (!grouped[date]) grouped[date] = [];
        grouped[date].push(t);
    }
    return grouped;
}

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
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
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

function editTransaction(id) {
    const transaction = currentTransactions.find(t => t.id === id);
    if (!transaction) return;

    document.getElementById('transaction-amount-edit').value = transaction.amount;
    document.getElementById('transaction-cost-edit').value = transaction.cost;
    document.getElementById('transaction-description-edit').value = transaction.description;
    document.getElementById('transaction-transaction-date-edit').value = transaction.transaction_date;
    document.getElementById('transactionModalEdit').dataset.editingId = id;
    document.getElementById('transactionModalEdit').style.display = 'flex';
}

document.getElementById('transactionSubmitEdit').addEventListener('click', async () => {
    const token = localStorage.getItem('token');
    const id = document.getElementById('transactionModalEdit').dataset.editingId;

    const updateData = {
        amount: Number(document.getElementById('transaction-amount-edit').value),
        cost: Number(document.getElementById('transaction-cost-edit').value),
        description: document.getElementById('transaction-description-edit').value,
        transaction_date: document.getElementById('transaction-transaction-date-edit').value,
    };

    const response = await fetch(`${API_URL}/transaction/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify(updateData),
    });

    if (!response.ok) {
        const errorData = await response.json();
        alert(errorData.detail || 'Ошибка при обновлении');
        return;
    }
    document.getElementById('transactionModalEdit').style.display = 'none';
    loadAndRenderTransactions();
});

async function deleteTransactionHandler(id) {
    if (!confirm('Удалить эту трату?')) return;
    const token = localStorage.getItem('token');

    const response = await fetch(`${API_URL}/transaction/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` },
    });

    if (!response.ok) {
        alert('Ошибка при удалении');
        return;
    }
    loadAndRenderTransactions();
}

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
    currentTransactions = transactions;
    document.getElementById('filter-rangeModal').style.display = 'none';
    renderTransactions(transactions);
});

document.addEventListener('DOMContentLoaded', () => {
    loadAndRenderTransactions();
});