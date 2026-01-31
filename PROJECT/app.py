import sqlite3
import random
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/order", methods=["GET", "POST"])
@login_required
def order():
    if request.method == "POST":
        conn=sqlite3.connect('project.db')
        conn.row_factory = sqlite3.Row  # Enable dictionary-like access
        cursor=conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM items")
        items = cursor.fetchone()[0]

        while(True):
            order_id=random.randint(1,1000)
            rows= cursor.execute(
                "SELECT * FROM order_description WHERE id = ?",
               (order_id,) ).fetchone()
            if rows is None:
                break
        for i in range(1,items+1):
            prod_qty="product{}-quantity".format(i)
            unit="product{}-unit".format(i)
            quantity = request.form.get(prod_qty, '0')  # Default to '0' if not provided
            try:
                quantity = int(quantity)
            except ValueError:
                quantity = 0  # Handle invalid input gracefully, e.g., default to 0

            item_name = cursor.execute(
                "SELECT name FROM items WHERE id = ?",
                (i,)
            ).fetchone()
            if quantity:
                qty_type=request.form.get(unit)
                query = "INSERT INTO order_description (id, item_id, quantity, qty_type, item_name) VALUES (?, ?, ?, ?, ?)"
                data = (
                    order_id ,i ,quantity ,qty_type, item_name["name"]
                )
                cursor.execute(query, data)
        query="SELECT * FROM order_description WHERE id = ?"
        data=(order_id,)
        order_list=cursor.execute(query, data)
        if order_list:
            customer_name=request.form.get("name")
            phone_no=request.form.get("phone")
            address=request.form.get("address")
            delivery_date=request.form.get("delivery_date")
            time=datetime.now()
            query = "INSERT INTO orders (user_id, order_id, name, date, order_status, delivery_address, delivery_date, phone_no) VALUES (?, ?, ?, ?, ? ,? ,? ,?)"
            data = (
                session["user_id"], order_id, customer_name, time, "REQUESTED", address, delivery_date, phone_no
            )
            cursor.execute(query, data)
            conn.commit()
            conn.close()
            return redirect("/")
        else:
           
            return apology("Please select some products")
        
    else:
        conn=sqlite3.connect('project.db')
        conn.row_factory = sqlite3.Row  # Enable dictionary-like access
        cursor=conn.cursor()
        items = cursor.execute("SELECT * FROM items").fetchall()
        conn.close()
        return render_template("order.html", items=items)

@app.route("/owner_dashboard", methods=["GET", "POST"])
@login_required 
def owner_dashboard():
    if request.method == "POST":
        if request.form.get("action") == "reject":
            conn=sqlite3.connect('project.db')
            conn.row_factory = sqlite3.Row  # Enable dictionary-like access
            cursor=conn.cursor()
            order_id=int(request.form.get("order_id"))
            cursor.execute("UPDATE orders SET order_status = 'REJECTED' WHERE order_id = ?", (order_id,))
            orders = cursor.execute("SELECT * FROM orders WHERE order_status = 'REQUESTED'").fetchall()
            order_description=cursor.execute("SELECT * FROM order_description WHERE id IN( SELECT order_id FROM orders WHERE order_status = 'REQUESTED' )").fetchall()
            deliveries = cursor.execute("SELECT * FROM orders WHERE order_status = 'TBD'").fetchall()
            delivery_description=cursor.execute("SELECT * FROM order_description WHERE id IN( SELECT order_id FROM orders WHERE order_status = 'TBD' )").fetchall()
            pending_payments = cursor.execute("SELECT * FROM orders WHERE order_status = 'APPROVED'").fetchall()
            pending_payments_description=cursor.execute("SELECT * FROM order_description WHERE id IN( SELECT order_id FROM orders WHERE order_status = 'APPROVED' )").fetchall()
            conn.commit()
            conn.close()
            return render_template("dashboard.html", orders=orders, items=order_description, deliveries=deliveries,descriptions=delivery_description,pending_payments=pending_payments,pending_descriptions=pending_payments_description)
        else:
            conn=sqlite3.connect('project.db')
            conn.row_factory = sqlite3.Row  # Enable dictionary-like access
            cursor=conn.cursor()
            order_id=int(request.form.get("order_id"))
            order_description=cursor.execute("SELECT * FROM order_description WHERE id = ?", (order_id,)).fetchall( )
            rows=cursor.execute("SELECT item_id FROM order_description WHERE id = ?", (order_id,)).fetchall()
            item_ids = [row[0] for row in rows]
            for i in item_ids:
                prd_prc="product{}_price".format(i)
                price = request.form.get(prd_prc, '0')
                try:
                    price = int(price)
                except ValueError:
                    price = 0
                if price == 0:
                    return apology("Put the prices in place")
                cursor.execute("UPDATE order_description SET price = ? WHERE  item_id = ? AND id = ?", (price, i, order_id))
            cursor.execute("UPDATE orders SET order_status = 'ACCEPTED' WHERE order_id = ?", (order_id,))
            total_bill=int(request.form.get("total-bill"))
            cursor.execute("UPDATE orders SET total_bill = ? WHERE order_id = ?",(total_bill, order_id))
            orders = cursor.execute("SELECT * FROM orders WHERE order_status = 'REQUESTED'").fetchall()
            order_description=cursor.execute("SELECT * FROM order_description WHERE id IN( SELECT order_id FROM orders WHERE order_status = 'REQUESTED' )").fetchall()
            deliveries = cursor.execute("SELECT * FROM orders WHERE order_status = 'TBD'").fetchall()
            delivery_description=cursor.execute("SELECT * FROM order_description WHERE id IN( SELECT order_id FROM orders WHERE order_status = 'TBD' )").fetchall()
            pending_payments = cursor.execute("SELECT * FROM orders WHERE order_status = 'APPROVED'").fetchall()
            pending_payments_description=cursor.execute("SELECT * FROM order_description WHERE id IN( SELECT order_id FROM orders WHERE order_status = 'APPROVED' )").fetchall()
            conn.commit()
            conn.close()
            return render_template("dashboard.html", orders=orders, items=order_description, deliveries=deliveries,descriptions=delivery_description,pending_payments=pending_payments,pending_descriptions=pending_payments_description  )
    else:       
        conn=sqlite3.connect('project.db')
        conn.row_factory = sqlite3.Row  # Enable dictionary-like access
        cursor=conn.cursor()
        orders = cursor.execute("SELECT * FROM orders WHERE order_status = 'REQUESTED'").fetchall()
        order_description=cursor.execute("SELECT * FROM order_description WHERE id IN( SELECT order_id FROM orders WHERE order_status = 'REQUESTED' )").fetchall()
        deliveries = cursor.execute("SELECT * FROM orders WHERE order_status = 'TBD'").fetchall()
        delivery_description=cursor.execute("SELECT * FROM order_description WHERE id IN( SELECT order_id FROM orders WHERE order_status = 'TBD' )").fetchall()
        pending_payments = cursor.execute("SELECT * FROM orders WHERE order_status = 'APPROVED'").fetchall()
        pending_payments_description=cursor.execute("SELECT * FROM order_description WHERE id IN( SELECT order_id FROM orders WHERE order_status = 'APPROVED' )").fetchall()
        conn.close()
        return render_template("dashboard.html", orders=orders, items=order_description, deliveries=deliveries,descriptions=delivery_description,pending_payments=pending_payments,pending_descriptions=pending_payments_description  )
      
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        conn=sqlite3.connect('project.db')
        conn.row_factory = sqlite3.Row  # Enable dictionary-like access
        cursor=conn.cursor()
        rows = cursor.execute(
            "SELECT * FROM owners WHERE username = ?", 
            (request.form.get("username"),)
        ).fetchone()
        # Ensure username exists and password is correct
        if  rows and check_password_hash(
            rows["password"], request.form.get("password")
        ): 
            session["user_id"] = rows["id"]
            conn.close()
            return redirect("/owner_dashboard")

       
        rows = cursor.execute(
            "SELECT * FROM users WHERE username = ?", 
            (request.form.get("username"),)
        ).fetchone()
        conn.close()
        # Ensure username exists and password is correct
        if not rows or not check_password_hash(
            rows["password"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/customer_dashboard", methods=["GET", "POST"])
@login_required
def customer_dashboard():
    if request.method == "POST":
        if request.form.get("action") == "reject":
            conn=sqlite3.connect('project.db')
            conn.row_factory = sqlite3.Row  # Enable dictionary-like access
            cursor=conn.cursor()
            order_id=int(request.form.get("order_id"))
            cursor.execute("UPDATE orders SET order_status = 'REJECTED' WHERE order_id = ?", (order_id,))
            user_id=int(session["user_id"])
            orders = cursor.execute("SELECT * FROM orders WHERE order_status = 'ACCEPTED' AND user_id = ?",(user_id,)).fetchall()
            order_description=cursor.execute("SELECT * FROM order_description WHERE id IN( SELECT order_id FROM orders WHERE order_status = 'ACCEPTED' AND user_id =  ? )",(user_id,)).fetchall()
            deliveries = cursor.execute("SELECT * FROM orders WHERE order_status = 'TBD' AND user_id = ?", (user_id,)).fetchall()
            delivery_description=cursor.execute("SELECT * FROM order_description WHERE id IN( SELECT order_id FROM orders WHERE order_status = 'TBD' AND user_id = ? )",(user_id,)).fetchall()
            pendings = cursor.execute("SELECT * FROM orders WHERE order_status = 'REQUESTED' AND user_id = ?", (user_id,)).fetchall()
            pending_descr=cursor.execute("SELECT * FROM order_description WHERE id IN( SELECT order_id FROM orders WHERE order_status = 'REQUESTED' AND user_id = ? )",(user_id,)).fetchall()
            conn.commit()
            conn.close()
            return render_template("customer_dashboard.html", orders=orders, items=order_description, deliveries=deliveries,descriptions=delivery_description,pendings=pendings, pending_descr=pending_descr  )

        else:
            conn=sqlite3.connect('project.db')
            conn.row_factory = sqlite3.Row  # Enable dictionary-like access
            cursor=conn.cursor()
            order_id=int(request.form.get("order_id"))
            cursor.execute("UPDATE orders SET order_status = 'APPROVED' WHERE order_id = ?", (order_id,))
            user_id=int(session["user_id"])
            orders = cursor.execute("SELECT * FROM orders WHERE order_status = 'ACCEPTED' AND user_id = ?",(user_id,)).fetchall()
            order_description=cursor.execute("SELECT * FROM order_description WHERE id IN( SELECT order_id FROM orders WHERE order_status = 'ACCEPTED' AND user_id =  ? )",(user_id,)).fetchall()
            deliveries = cursor.execute("SELECT * FROM orders WHERE order_status = 'TBD' AND user_id = ?", (user_id,)).fetchall()
            delivery_description=cursor.execute("SELECT * FROM order_description WHERE id IN( SELECT order_id FROM orders WHERE order_status = 'TBD' AND user_id = ? )",(user_id,)).fetchall()
            pendings = cursor.execute("SELECT * FROM orders WHERE order_status = 'REQUESTED' AND user_id = ?", (user_id,)).fetchall()
            pending_descr=cursor.execute("SELECT * FROM order_description WHERE id IN( SELECT order_id FROM orders WHERE order_status = 'REQUESTED' AND user_id = ? )",(user_id,)).fetchall()
            conn.commit()
            conn.close()
            return render_template("customer_dashboard.html", orders=orders, items=order_description, deliveries=deliveries,descriptions=delivery_description,pendings=pendings, pending_descr=pending_descr  )
    
    else:       
        conn=sqlite3.connect('project.db')
        conn.row_factory = sqlite3.Row  # Enable dictionary-like access
        cursor=conn.cursor()
        user_id=int(session["user_id"])
        orders = cursor.execute("SELECT * FROM orders WHERE order_status = 'ACCEPTED' AND user_id = ?",(user_id,)).fetchall()
        order_description=cursor.execute("SELECT * FROM order_description WHERE id IN( SELECT order_id FROM orders WHERE order_status = 'ACCEPTED' AND user_id =  ? )",(user_id,)).fetchall()
        deliveries = cursor.execute("SELECT * FROM orders WHERE order_status = 'TBD' AND user_id = ?", (user_id,)).fetchall()
        delivery_description=cursor.execute("SELECT * FROM order_description WHERE id IN( SELECT order_id FROM orders WHERE order_status = 'TBD' AND user_id = ? )",(user_id,)).fetchall()
        pendings = cursor.execute("SELECT * FROM orders WHERE order_status = 'REQUESTED' AND user_id = ?", (user_id,)).fetchall()
        pending_descr=cursor.execute("SELECT * FROM order_description WHERE id IN( SELECT order_id FROM orders WHERE order_status = 'REQUESTED' AND user_id = ? )",(user_id,)).fetchall()
        conn.close()
        return render_template("customer_dashboard.html", orders=orders, items=order_description, deliveries=deliveries,descriptions=delivery_description,pendings=pendings, pending_descr=pending_descr  )

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Check if passwords match
        if request.form.get("password") != request.form.get("confirm-password"):
            return apology("Passwords do not match", 400)

        # Connect to the database
        conn = sqlite3.connect('project.db')
        conn.row_factory = sqlite3.Row  # Enable dictionary-like access
        cursor = conn.cursor()

        try:
            # Insert the new user
            query = "INSERT INTO users (username, password) VALUES (?, ?)"
            data = (
                request.form.get("username"),
                generate_password_hash(request.form.get("password"))
            )
            cursor.execute(query, data)
            conn.commit()

            # Fetch the newly created user
            user = cursor.execute(
                "SELECT * FROM users WHERE username = ?",
                (request.form.get("username"),)
            ).fetchone()

            # Log the user in
            session["user_id"] = user["id"]

        except sqlite3.IntegrityError:  # Handle duplicate username
            conn.close()
            return apology("Username already exists", 400)

        finally:
            conn.close()

        # Redirect to the home page
        return redirect("/")

    # Render signup page on GET
    else:
        return render_template("signup.html")


@app.route("/TBD", methods=["GET", "POST"])
@login_required
def TBD():
   if request.method == "POST":
        if request.form.get("action") == "reject":
            conn=sqlite3.connect('project.db')
            conn.row_factory = sqlite3.Row  # Enable dictionary-like access
            cursor=conn.cursor()
            order_id=int(request.form.get("order_id"))
            cursor.execute("UPDATE orders SET order_status = 'REJECTED' WHERE order_id = ?", (order_id,))
            orders = cursor.execute("SELECT * FROM orders WHERE order_status = 'REQUESTED'").fetchall()
            order_description=cursor.execute("SELECT * FROM order_description WHERE id IN( SELECT order_id FROM orders WHERE order_status = 'REQUESTED' )").fetchall()
            deliveries = cursor.execute("SELECT * FROM orders WHERE order_status = 'TBD'").fetchall()
            delivery_description=cursor.execute("SELECT * FROM order_description WHERE id IN( SELECT order_id FROM orders WHERE order_status = 'TBD' )").fetchall()
            pending_payments = cursor.execute("SELECT * FROM orders WHERE order_status = 'APPROVED'").fetchall()
            pending_payments_description=cursor.execute("SELECT * FROM order_description WHERE id IN( SELECT order_id FROM orders WHERE order_status = 'APPROVED' )").fetchall()
            conn.commit()
            conn.close()
            return render_template("dashboard.html", orders=orders, items=order_description, deliveries=deliveries,descriptions=delivery_description,pending_payments=pending_payments,pending_descriptions=pending_payments_description  )
        else:
            conn=sqlite3.connect('project.db')
            conn.row_factory = sqlite3.Row  # Enable dictionary-like access
            cursor=conn.cursor()
            order_id=int(request.form.get("order_id"))
            cursor.execute("UPDATE orders SET order_status = 'TBD' WHERE order_id = ?", (order_id,))
            orders = cursor.execute("SELECT * FROM orders WHERE order_status = 'REQUESTED'").fetchall()
            order_description=cursor.execute("SELECT * FROM order_description WHERE id IN( SELECT order_id FROM orders WHERE order_status = 'REQUESTED' )").fetchall()
            deliveries = cursor.execute("SELECT * FROM orders WHERE order_status = 'TBD'").fetchall()
            delivery_description=cursor.execute("SELECT * FROM order_description WHERE id IN( SELECT order_id FROM orders WHERE order_status = 'TBD' )").fetchall()
            pending_payments = cursor.execute("SELECT * FROM orders WHERE order_status = 'APPROVED'").fetchall()
            pending_payments_description=cursor.execute("SELECT * FROM order_description WHERE id IN( SELECT order_id FROM orders WHERE order_status = 'APPROVED' )").fetchall()
            conn.commit()
            conn.close()
            return render_template("dashboard.html", orders=orders, items=order_description, deliveries=deliveries,descriptions=delivery_description,pending_payments=pending_payments,pending_descriptions=pending_payments_description  )
    