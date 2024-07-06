DROP TABLE IF EXISTS customers;

CREATE TABLE IF NOT EXISTS customers AS TABLE data_2023_jan WITH NO DATA;

INSERT INTO customers SELECT * FROM data_2022_oct;
INSERT INTO customers SELECT * FROM data_2022_nov;
INSERT INTO customers SELECT * FROM data_2022_dec;
INSERT INTO customers SELECT * FROM data_2023_jan;
INSERT INTO customers SELECT * FROM data_2023_feb;

SELECT COUNT(*) FROM customers;
