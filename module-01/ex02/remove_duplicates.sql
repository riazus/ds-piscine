-- get duplicates count
SELECT COUNT(*) as duplicates
FROM (
    SELECT COUNT(*) as duplicates 
    FROM customers
    GROUP BY event_time, event_type, product_id, price, user_id, user_session
    HAVING COUNT(*) > 1
) AS subquery;


-- add a primary key column if it does not exist
ALTER TABLE customers ADD COLUMN IF NOT EXISTS id SERIAL PRIMARY KEY;

-- use a CTE to identify duplicate rows
WITH duplicates AS (
    SELECT id
    FROM (
        SELECT id,
               ROW_NUMBER() OVER (PARTITION BY event_time, event_type, product_id, price, user_id, user_session ORDER BY id) AS row_num
        FROM customers
    ) t
    WHERE t.row_num > 1
)

-- delete the duplicate rows
DELETE FROM customers
USING duplicates
WHERE customers.id = duplicates.id;

ALTER TABLE customers DROP COLUMN id;


-- get duplicates count
SELECT COUNT(*) as duplicates
FROM (
    SELECT COUNT(*) as duplicates 
    FROM customers
    GROUP BY event_time, event_type, product_id, price, user_id, user_session
    HAVING COUNT(*) > 1
) AS subquery;