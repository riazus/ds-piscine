ALTER TABLE IF EXISTS public.customers
    ADD COLUMN category_id bigint;

ALTER TABLE IF EXISTS public.customers
    ADD COLUMN category_code text;

ALTER TABLE IF EXISTS public.customers
    ADD COLUMN brand text;

UPDATE customers AS cus
SET
    category_id = it.category_id,
    category_code = it.category_code,
    brand = it.brand
FROM items AS it
WHERE it.product_id = cus.product_id;
