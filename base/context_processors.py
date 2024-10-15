# base/context_processors.py

from django.db import connection
from django.contrib.auth.decorators import login_required


def cart_item_count(request):
    count = 0  # Default count
    if request.user.is_authenticated:
        customer_id = request.user.customer.id  # Get the customer ID
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT SUM(ci.quantity) AS total_quantity
                FROM base_cartitem ci
                JOIN base_cart c ON ci.cart_id = c.id
                WHERE c.user_id = %s;
                """,
                [customer_id],
            )
            row = cursor.fetchone()
            count = (
                row[0] if row and row[0] is not None else 0
            )  # Default to 0 if no items
    return {"item_count": count}
