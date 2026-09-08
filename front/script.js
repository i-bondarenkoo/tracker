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

document.querySelector('.add-transaction-btn').addEventListener('click', ()=>{
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