from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import (
    Customer,
    Category,
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Address,
)


media_url = settings.MEDIA_URL


# Utility function to execute raw SQL and return results
def execute_sql(query, params=()):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def homepage(self):
    featured_products = Product.objects.all()[:10]
    context = {"featured_products": featured_products}
    return render(self, "base/homepage.html", context)


# View to display all products
def product_list(request):
    search_query = request.GET.get("search", "")
    sort_option = request.GET.get("sort", "name_asc")  # Default sort option

    print("SEARCH QUERY:", search_query)

    # Map user-friendly sort options to database fields and order
    sort_mapping = {
        "price_asc": ("unit_price", "ASC"),
        "price_desc": ("unit_price", "DESC"),
        "name_asc": ("name", "ASC"),
        "name_desc": ("name", "DESC"),
    }

    # Get the sort field and order from the mapping
    sort_by, sort_order = sort_mapping.get(sort_option, ("name", "ASC"))

    # Fetch products with search and sort
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT id, name, description, unit_price, stock, CONCAT('{media_url}', image) AS image
            FROM base_product
            WHERE name LIKE %s
            ORDER BY {sort_by} {sort_order};
            """,
            [f"%{search_query}%"],  # Use parameterized query to prevent SQL injection
        )
        products = cursor.fetchall()
        print(products)

    # Fetch categories
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, name
            FROM base_category;
            """
        )
        categories = cursor.fetchall()

    return render(
        request,
        "base/product_list.html",
        {
            "products": products,
            "categories": categories,
            "search_query": search_query,
            "sort_option": sort_option,
        },
    )


# View to display details of a single product
def product_detail(request, product_id):
    query = f"""
        SELECT p.id, p.name, p.description, p.unit_price, p.stock, CONCAT('{media_url}', p.image) AS image, c.name as category_name
        FROM base_product p
        JOIN base_category c ON p.category_id = c.id
        WHERE p.id = %s
    """
    product = execute_sql(query, [product_id])[0]
    return render(request, "base/product_detail.html", {"product": product})


# View to display products by category
def product_by_category(request, category_id):
    query = f"""
        SELECT p.id, p.name, p.description, p.unit_price, p.stock, CONCAT('{media_url}', p.image) AS image, c.name as category_name
        FROM base_product p
        JOIN base_category c ON p.category_id = c.id
        WHERE c.id = %s
    """
    products = execute_sql(query, [category_id])
    return render(request, "base/product_by_category.html", {"products": products})


@login_required(login_url="login")
def view_cart(request):
    # Get the Customer object related to the logged-in user
    customer = Customer.objects.get(user=request.user)

    with connection.cursor() as cursor:
        # Query to get the cart items for the customer
        # Mahfuj start
        cursor.execute(
            f"""
            SELECT ci.id, p.name, CONCAT('{media_url}', p.image) AS image, ci.quantity, p.unit_price,
                   ci.quantity * p.unit_price AS total_price
            FROM base_cartitem ci
            JOIN base_product p ON ci.product_id = p.id
            JOIN base_cart c ON ci.cart_id = c.id
            WHERE c.user_id = %s;  -- Use the customer ID here
            """,
            [customer.id],  # Pass the customer ID
        )
        # Mahfuj end

        cart_items = cursor.fetchall()

    # Use another query to calculate the total price
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT SUM(ci.quantity * p.unit_price) AS total
            FROM base_cartitem ci
            JOIN base_product p ON ci.product_id = p.id
            JOIN base_cart c ON ci.cart_id = c.id
            WHERE c.user_id = %s;  -- Use the customer ID here
            """,
            [customer.id],  # Pass the customer ID
        )

        total = (
            cursor.fetchone()[0] or 0
        )  # Get the total from the query, default to 0 if None

    return render(request, "base/cart.html", {"cart_items": cart_items, "total": total})


def add_to_cart(request, product_id):
    user = request.user

    # Get the customer associated with the logged-in user
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM base_customer WHERE user_id = %s", [user.id])
        customer_row = cursor.fetchone()

    if not customer_row:
        return redirect("login")

    customer_id = customer_row[0]

    # Check if the cart already exists for this customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM base_cart WHERE user_id = %s", [customer_id])
        cart_row = cursor.fetchone()

    if cart_row:
        cart_id = cart_row[0]
    else:
        # Create a new cart if one does not exist
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO base_cart (user_id, created_at, updated_at) VALUES (%s, datetime('now'), datetime('now'))",
                [customer_id],
            )
            cart_id = cursor.lastrowid

    # Check if the product already exists in the cart
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, quantity FROM base_cartitem WHERE cart_id = %s AND product_id = %s",
            [cart_id, product_id],
        )
        cart_item_row = cursor.fetchone()

    if cart_item_row:
        # Update the quantity if the product is already in the cart
        cart_item_id = cart_item_row[0]
        quantity = cart_item_row[1] + 1

        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE base_cartitem SET quantity = %s WHERE id = %s",
                [quantity, cart_item_id],
            )
    else:
        # Add the product to the cart if it does not exist
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO base_cartitem (cart_id, product_id, quantity) VALUES (%s, %s, 1)",
                [cart_id, product_id],
            )

    return redirect("view_cart")


@login_required
def remove_from_cart(request, cart_item_id):
    # Get the Customer object related to the logged-in user
    customer = Customer.objects.get(user=request.user)

    with connection.cursor() as cursor:
        # Execute the delete query
        # Nasif start
        cursor.execute(
            """
            DELETE FROM base_cartitem
            WHERE id = %s AND cart_id IN (
                SELECT id FROM base_cart WHERE user_id = %s
            );
            """,
            [cart_item_id, customer.id],
        )
        # Nasif end

    # Redirect back to the cart view
    return redirect(
        "view_cart"
    )  # Change 'view_cart' to the appropriate URL name if necessary
