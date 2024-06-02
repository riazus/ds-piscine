CREATE TYPE public.event_type_enum AS ENUM
    ('remove_from_cart', 'view', 'cart', 'purchase');

CREATE TABLE public.data_2022_dec (
    event_time DATE,
    event_type event_type_enum,
    product_id VARCHAR(255),
    price DECIMAL,
    user_id INTEGER,
    user_session UUID
);

CREATE TABLE public.data_2022_nov (
    event_time DATE,
    event_type event_type_enum,
    product_id VARCHAR(255),
    price DECIMAL,
    user_id INTEGER,
    user_session UUID
);

CREATE TABLE public.data_2022_oct (
    event_time DATE,
    event_type event_type_enum,
    product_id VARCHAR(255),
    price DECIMAL,
    user_id INTEGER,
    user_session UUID
);

CREATE TABLE public.data_2023_jan (
    event_time DATE,
    event_type event_type_enum,
    product_id VARCHAR(255),
    price DECIMAL,
    user_id INTEGER,
    user_session UUID
);

CREATE TABLE public.items
(
    product_id integer NOT NULL,
    category_id text NOT NULL,
    category_code text,
    brand text NOT NULL,
    PRIMARY KEY (product_id)
);
