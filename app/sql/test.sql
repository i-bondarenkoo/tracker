SELECT users.first_name AS users_first_name, users.last_name AS users_last_name, users.email AS users_email, 
users.password_hash AS users_password_hash, users.created_at AS users_created_at, users.id AS users_id 
FROM users 
WHERE users.id = $1::INTEGER 10

SELECT transactions.category_id, sum(transactions.cost * transactions.amount) AS sum_1 
FROM transactions 
WHERE transactions.user_id = $1::INTEGER AND transactions.transaction_date BETWEEN $2::DATE AND $3::DATE GROUP BY transactions.category_id
(10, datetime.date(2026, 8, 1), datetime.date(2026, 8, 31))

SELECT transactions.category_id, sum(transactions.cost * transactions.amount) AS sum_1 
FROM transactions 
WHERE transactions.user_id = $1::INTEGER AND transactions.transaction_date BETWEEN $2::DATE AND $3::DATE GROUP BY transactions.category_id
(10, datetime.date(2026, 9, 1), datetime.date(2026, 9, 30))

SELECT categories.name, categories.user_id, categories.id 
FROM categories 
WHERE categories.id IN ($1::INTEGER, $2::INTEGER, $3::INTEGER, $4::INTEGER, $5::INTEGER, $6::INTEGER)
(5, 6, 7, 9, 27, 28)
