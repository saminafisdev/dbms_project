## Fetching Products

```sql
SELECT id, name, description, unit_price, stock, CONCAT('{media_url}', image) AS image
FROM base_product;
```

`media_url` is a Python variable

## Fetching Product Detail

```sql
SELECT p.id, p.name, p.description, p.unit_price, p.stock, CONCAT('{media_url}', p.image) AS image, c.name as category_name
FROM base_product p
JOIN base_category c ON p.category_id = c.id
WHERE p.id = %s
```

where `%s` is the placeholder for `product_id`

## View cart

```sql
SELECT ci.id, p.name, CONCAT('{media_url}', p.image) AS image, ci.quantity, p.unit_price,
      ci.quantity * p.unit_price AS total_price
FROM base_cartitem ci
JOIN base_product p ON ci.product_id = p.id
JOIN base_cart c ON ci.cart_id = c.id
WHERE c.user_id = %s;  -- Use the customer ID here
```

where `%s` is the customer ID fetched using Python

### Calculate total price

```sql
SELECT SUM(ci.quantity * p.unit_price) AS total
FROM base_cartitem ci
JOIN base_product p ON ci.product_id = p.id
JOIN base_cart c ON ci.cart_id = c.id
WHERE c.user_id = %s;  -- Use the customer ID here
```

where `%s` is the customer ID fetched using Python

## Add to cart

Get the customer id

```sql
SELECT id FROM base_customer WHERE user_id = %s
```

Check if the cart already exists for this customer

```sql
SELECT id FROM base_cart WHERE user_id = %s
```

Create a new cart if one does not exist

```sql
INSERT INTO base_cart (user_id, created_at, updated_at) VALUES (%s, datetime('now'), datetime('now'))
```

Check if the product already exists in the cart

```sql
SELECT id, quantity FROM base_cartitem WHERE cart_id = %s AND product_id = %s
```

Update the quantity if the product is already in the cart

```sql
UPDATE base_cartitem SET quantity = %s WHERE id = %s
```

Add the product to the cart if it does not exist

```sql
INSERT INTO base_cartitem (cart_id, product_id, quantity) VALUES (%s, %s, 1)
```

## Remove from cart

```sql
DELETE FROM base_cartitem
WHERE id = %s AND cart_id IN (
  SELECT id FROM base_cart WHERE user_id = %s
);
```
