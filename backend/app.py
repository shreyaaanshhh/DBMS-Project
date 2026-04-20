import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from db import query

app = Flask(__name__)


def get_allowed_origins():
    raw = os.getenv("CORS_ORIGINS", "*").strip()
    if not raw or raw == "*":
        return "*"
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


CORS(app, origins=get_allowed_origins())

def ok(data):
    return jsonify({"success": True, "data": data})

def err(msg, code=400):
    return jsonify({"success": False, "error": msg}), code


@app.route("/", methods=["GET"])
def root():
    return ok({"message": "Restaurant Chain Management API", "status": "running"})


@app.route("/health", methods=["GET"])
def health():
    return ok({"status": "healthy"})


# ══════════════════════════════════════════════════════════════
# BRANCHES
# ══════════════════════════════════════════════════════════════

@app.route("/branches", methods=["GET"])
def get_branches():
    rows = query("SELECT * FROM Branch ORDER BY city, name")
    return ok(rows)

@app.route("/branches/<int:bid>", methods=["GET"])
def get_branch(bid):
    rows = query("SELECT * FROM Branch WHERE branch_id = %s", (bid,))
    if not rows:
        return err("Branch not found", 404)
    return ok(rows[0])

@app.route("/branches", methods=["POST"])
def add_branch():
    d = request.json
    res = query(
        "INSERT INTO Branch (name, city, address, phone, manager_name) VALUES (%s,%s,%s,%s,%s)",
        (d["name"], d["city"], d["address"], d.get("phone"), d.get("manager_name")),
        fetch=False,
    )
    return ok({"branch_id": res["last_id"]}), 201

@app.route("/branches/<int:bid>", methods=["PUT"])
def update_branch(bid):
    d = request.json
    query(
        "UPDATE Branch SET name=%s, city=%s, address=%s, phone=%s, manager_name=%s WHERE branch_id=%s",
        (d["name"], d["city"], d["address"], d.get("phone"), d.get("manager_name"), bid),
        fetch=False,
    )
    return ok({"updated": bid})

@app.route("/branches/<int:bid>", methods=["DELETE"])
def delete_branch(bid):
    query("DELETE FROM Branch WHERE branch_id = %s", (bid,), fetch=False)
    return ok({"deleted": bid})


# ══════════════════════════════════════════════════════════════
# CUSTOMERS
# ══════════════════════════════════════════════════════════════

@app.route("/customers", methods=["GET"])
def get_customers():
    rows = query("SELECT * FROM Customer ORDER BY name")
    return ok(rows)

@app.route("/customers/<int:cid>", methods=["GET"])
def get_customer(cid):
    rows = query("SELECT * FROM Customer WHERE customer_id = %s", (cid,))
    if not rows:
        return err("Customer not found", 404)
    return ok(rows[0])

@app.route("/customers", methods=["POST"])
def add_customer():
    d = request.json
    res = query(
        "INSERT INTO Customer (name, email, phone, city) VALUES (%s,%s,%s,%s)",
        (d["name"], d["email"], d.get("phone"), d.get("city")),
        fetch=False,
    )
    return ok({"customer_id": res["last_id"]}), 201

@app.route("/customers/<int:cid>/orders", methods=["GET"])
def customer_orders(cid):
    rows = query(
        """SELECT o.order_id, b.name AS branch, o.order_type, o.status,
                  p.amount, p.method, o.ordered_at
           FROM `Order` o
           JOIN Branch b ON o.branch_id = b.branch_id
           LEFT JOIN Payment p ON o.order_id = p.order_id
           WHERE o.customer_id = %s
           ORDER BY o.ordered_at DESC""",
        (cid,),
    )
    return ok(rows)


# ══════════════════════════════════════════════════════════════
# MENU
# ══════════════════════════════════════════════════════════════

@app.route("/menu", methods=["GET"])
def get_menu():
    branch_id = request.args.get("branch_id")
    if branch_id:
        rows = query(
            "SELECT * FROM Menu_Item WHERE branch_id = %s AND is_available = TRUE ORDER BY category, name",
            (branch_id,),
        )
    else:
        rows = query("SELECT * FROM Menu_Item WHERE is_available = TRUE ORDER BY branch_id, category, name")
    return ok(rows)

@app.route("/menu", methods=["POST"])
def add_menu_item():
    d = request.json
    res = query(
        "INSERT INTO Menu_Item (branch_id, name, category, price) VALUES (%s,%s,%s,%s)",
        (d["branch_id"], d["name"], d["category"], d["price"]),
        fetch=False,
    )
    return ok({"item_id": res["last_id"]}), 201

@app.route("/menu/<int:iid>", methods=["PUT"])
def update_menu_item(iid):
    d = request.json
    query(
        "UPDATE Menu_Item SET name=%s, category=%s, price=%s, is_available=%s WHERE item_id=%s",
        (d["name"], d["category"], d["price"], d.get("is_available", True), iid),
        fetch=False,
    )
    return ok({"updated": iid})

@app.route("/menu/<int:iid>", methods=["DELETE"])
def delete_menu_item(iid):
    query("UPDATE Menu_Item SET is_available = FALSE WHERE item_id = %s", (iid,), fetch=False)
    return ok({"deactivated": iid})


# ══════════════════════════════════════════════════════════════
# INVENTORY
# ══════════════════════════════════════════════════════════════

@app.route("/inventory", methods=["GET"])
def get_inventory():
    branch_id = request.args.get("branch_id")
    if branch_id:
        rows = query(
            "SELECT i.*, b.name AS branch FROM Inventory i JOIN Branch b ON i.branch_id=b.branch_id WHERE i.branch_id=%s ORDER BY i.ingredient",
            (branch_id,),
        )
    else:
        rows = query(
            "SELECT i.*, b.name AS branch FROM Inventory i JOIN Branch b ON i.branch_id=b.branch_id ORDER BY b.name, i.ingredient"
        )
    return ok(rows)

@app.route("/inventory/alerts", methods=["GET"])
def low_stock_alerts():
    rows = query(
        """SELECT b.name AS branch, i.ingredient, i.quantity, i.unit, i.reorder_level
           FROM Inventory i JOIN Branch b ON i.branch_id = b.branch_id
           WHERE i.quantity <= i.reorder_level
           ORDER BY b.name, i.ingredient"""
    )
    return ok(rows)

@app.route("/inventory", methods=["POST"])
def add_inventory():
    d = request.json
    res = query(
        "INSERT INTO Inventory (branch_id, ingredient, quantity, unit, reorder_level) VALUES (%s,%s,%s,%s,%s)",
        (d["branch_id"], d["ingredient"], d["quantity"], d["unit"], d["reorder_level"]),
        fetch=False,
    )
    return ok({"inventory_id": res["last_id"]}), 201

@app.route("/inventory/<int:iid>", methods=["PUT"])
def update_inventory(iid):
    d = request.json
    query(
        "UPDATE Inventory SET quantity=%s, reorder_level=%s WHERE inventory_id=%s",
        (d["quantity"], d.get("reorder_level"), iid),
        fetch=False,
    )
    return ok({"updated": iid})


# ══════════════════════════════════════════════════════════════
# ORDERS
# ══════════════════════════════════════════════════════════════

@app.route("/orders", methods=["GET"])
def get_orders():
    branch_id = request.args.get("branch_id")
    status    = request.args.get("status")
    sql = """SELECT o.order_id, b.name AS branch, c.name AS customer,
                    o.order_type, o.status, o.ordered_at,
                    p.amount, p.method, p.status AS payment_status
             FROM `Order` o
             JOIN Branch b   ON o.branch_id   = b.branch_id
             JOIN Customer c ON o.customer_id = c.customer_id
             LEFT JOIN Payment p ON o.order_id = p.order_id
             WHERE 1=1"""
    params = []
    if branch_id:
        sql += " AND o.branch_id = %s"
        params.append(branch_id)
    if status:
        sql += " AND o.status = %s"
        params.append(status)
    sql += " ORDER BY o.ordered_at DESC"
    rows = query(sql, tuple(params))
    return ok(rows)

@app.route("/orders/<int:oid>", methods=["GET"])
def get_order(oid):
    order = query(
        """SELECT o.*, b.name AS branch, c.name AS customer
           FROM `Order` o
           JOIN Branch b   ON o.branch_id   = b.branch_id
           JOIN Customer c ON o.customer_id = c.customer_id
           WHERE o.order_id = %s""",
        (oid,),
    )
    if not order:
        return err("Order not found", 404)
    items = query(
        """SELECT oi.*, mi.name AS item_name, mi.category
           FROM Order_Item oi JOIN Menu_Item mi ON oi.item_id = mi.item_id
           WHERE oi.order_id = %s""",
        (oid,),
    )
    payment = query("SELECT * FROM Payment WHERE order_id = %s", (oid,))
    result = order[0]
    result["items"]   = items
    result["payment"] = payment[0] if payment else None
    return ok(result)

@app.route("/orders", methods=["POST"])
def place_order():
    d = request.json
    # Create order
    res = query(
        "INSERT INTO `Order` (branch_id, customer_id, order_type) VALUES (%s,%s,%s)",
        (d["branch_id"], d["customer_id"], d["order_type"]),
        fetch=False,
    )
    order_id = res["last_id"]
    # Insert items
    for item in d["items"]:
        price_row = query("SELECT price FROM Menu_Item WHERE item_id=%s", (item["item_id"],))
        if not price_row:
            return err(f"Item {item['item_id']} not found", 404)
        unit_price = price_row[0]["price"]
        query(
            "INSERT INTO Order_Item (order_id, item_id, quantity, unit_price) VALUES (%s,%s,%s,%s)",
            (order_id, item["item_id"], item["quantity"], unit_price),
            fetch=False,
        )
    return ok({"order_id": order_id}), 201

@app.route("/orders/<int:oid>/status", methods=["PATCH"])
def update_order_status(oid):
    d = request.json
    valid = ["Pending", "Preparing", "Ready", "Delivered", "Cancelled"]
    if d.get("status") not in valid:
        return err(f"Status must be one of {valid}")
    query("UPDATE `Order` SET status=%s WHERE order_id=%s", (d["status"], oid), fetch=False)
    return ok({"order_id": oid, "status": d["status"]})


# ══════════════════════════════════════════════════════════════
# PAYMENTS
# ══════════════════════════════════════════════════════════════

@app.route("/payments", methods=["POST"])
def make_payment():
    d = request.json
    # Calculate total from order items
    rows = query(
        "SELECT SUM(quantity * unit_price) AS total FROM Order_Item WHERE order_id = %s",
        (d["order_id"],),
    )
    total = float(rows[0]["total"] or 0)
    res = query(
        "INSERT INTO Payment (order_id, amount, method, status) VALUES (%s,%s,%s,'Paid')",
        (d["order_id"], total, d["method"]),
        fetch=False,
    )
    # Auto mark order as delivered on payment
    query(
        "UPDATE `Order` SET status='Delivered' WHERE order_id=%s AND status != 'Cancelled'",
        (d["order_id"],), fetch=False
    )
    return ok({"payment_id": res["last_id"], "amount": total}), 201

@app.route("/payments/<int:oid>", methods=["GET"])
def get_payment(oid):
    rows = query("SELECT * FROM Payment WHERE order_id = %s", (oid,))
    if not rows:
        return err("Payment not found", 404)
    return ok(rows[0])


# ══════════════════════════════════════════════════════════════
# REVIEWS
# ══════════════════════════════════════════════════════════════

@app.route("/reviews", methods=["GET"])
def get_reviews():
    branch_id = request.args.get("branch_id")
    if branch_id:
        rows = query(
            """SELECT r.*, c.name AS customer FROM Review r
               JOIN Customer c ON r.customer_id = c.customer_id
               WHERE r.branch_id = %s ORDER BY r.reviewed_at DESC""",
            (branch_id,),
        )
    else:
        rows = query(
            """SELECT r.*, c.name AS customer, b.name AS branch FROM Review r
               JOIN Customer c ON r.customer_id = c.customer_id
               JOIN Branch b   ON r.branch_id   = b.branch_id
               ORDER BY r.reviewed_at DESC"""
        )
    return ok(rows)

@app.route("/reviews", methods=["POST"])
def add_review():
    d = request.json
    order = query("SELECT * FROM `Order` WHERE order_id=%s AND customer_id=%s", (d["order_id"], d["customer_id"]))
    if not order:
        return err("Order not found or doesn't belong to this customer", 403)
    res = query(
        "INSERT INTO Review (order_id, customer_id, branch_id, rating, comment) VALUES (%s,%s,%s,%s,%s)",
        (d["order_id"], d["customer_id"], order[0]["branch_id"], d["rating"], d.get("comment", "")),
        fetch=False,
    )
    return ok({"review_id": res["last_id"]}), 201


# ══════════════════════════════════════════════════════════════
# ANALYTICS
# ══════════════════════════════════════════════════════════════

@app.route("/analytics/top-items", methods=["GET"])
def top_items():
    rows = query(
        """SELECT mi.name AS item, mi.category,
                  SUM(oi.quantity) AS total_sold,
                  SUM(oi.quantity * oi.unit_price) AS revenue
           FROM Order_Item oi JOIN Menu_Item mi ON oi.item_id = mi.item_id
           GROUP BY mi.item_id, mi.name, mi.category
           ORDER BY total_sold DESC LIMIT 10"""
    )
    return ok(rows)

@app.route("/analytics/branch-revenue", methods=["GET"])
def branch_revenue():
    rows = query(
        """SELECT b.name AS branch, b.city,
                  COUNT(DISTINCT o.order_id) AS total_orders,
                  COALESCE(SUM(p.amount), 0) AS total_revenue
           FROM Branch b
           LEFT JOIN `Order` o  ON b.branch_id = o.branch_id
           LEFT JOIN Payment p  ON o.order_id  = p.order_id AND p.status = 'Paid'
           GROUP BY b.branch_id, b.name, b.city
           ORDER BY total_revenue DESC"""
    )
    return ok(rows)

@app.route("/analytics/ratings", methods=["GET"])
def branch_ratings():
    rows = query(
        """SELECT b.name AS branch, b.city,
                  ROUND(AVG(r.rating), 2) AS avg_rating,
                  COUNT(r.review_id) AS total_reviews
           FROM Branch b
           LEFT JOIN Review r ON b.branch_id = r.branch_id
           GROUP BY b.branch_id, b.name, b.city
           ORDER BY avg_rating DESC"""
    )
    return ok(rows)

@app.route("/analytics/payment-methods", methods=["GET"])
def payment_methods():
    rows = query(
        """SELECT method, COUNT(*) AS transactions, SUM(amount) AS total
           FROM Payment WHERE status='Paid'
           GROUP BY method ORDER BY total DESC"""
    )
    return ok(rows)

@app.route("/analytics/summary", methods=["GET"])
def summary():
    total_revenue = query("SELECT COALESCE(SUM(amount),0) AS v FROM Payment WHERE status='Paid'")[0]["v"]
    total_orders  = query("SELECT COUNT(*) AS v FROM `Order`")[0]["v"]
    total_customers = query("SELECT COUNT(*) AS v FROM Customer")[0]["v"]
    total_branches  = query("SELECT COUNT(*) AS v FROM Branch")[0]["v"]
    alerts = query("SELECT COUNT(*) AS v FROM Inventory WHERE quantity <= reorder_level")[0]["v"]
    return ok({
        "total_revenue":   float(total_revenue),
        "total_orders":    total_orders,
        "total_customers": total_customers,
        "total_branches":  total_branches,
        "low_stock_alerts": alerts,
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
