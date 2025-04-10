-- migrate:up
CREATE TABLE product_track_views (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(10) REFERENCES products(sku),
    keyword VARCHAR(100),
    viewed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- migrate:down
DROP TABLE IF EXISTS product_track_views;
