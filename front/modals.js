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
document.getElementById('transactionCloseEdit').addEventListener('click', () => {
    document.getElementById('transactionModalEdit').style.display = 'none';
});

document.querySelector('.stats-btn').addEventListener('click', () => {
    document.getElementById('statsModal').style.display = 'flex';
});
document.getElementById('statsClose').addEventListener('click', ()=> {
    document.getElementById('statsModal').style.display = 'none';
});