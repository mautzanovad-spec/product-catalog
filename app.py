from flask import Flask, render_template, request, redirect, url_for
import requests
from db import init_db, get_db

app = Flask(__name__)


@app.route("/")
def index():
    url = "https://fakestoreapi.com/products"
    res = requests.get(url)
    products = res.json()
    return render_template("index.html", products=products)


@app.route("/add_favorite/<int:product_id>")
def add_favorite(product_id):
    url = f"https://fakestoreapi.com/products/{product_id}"
    res = requests.get(url)
    p = res.json()

    con = get_db()
    cur = con.cursor()

    cur.execute("""
        INSERT OR IGNORE INTO favorites (product_id, title, price, category, image)
        VALUES (?, ?, ?, ?, ?)
    """, (p["id"], p["title"], p["price"], p["category"], p["image"]))

    con.commit()
    con.close()

    return redirect(url_for("index"))


@app.route("/favorites")
def favorites():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM favorites")
    items = cur.fetchall()
    con.close()

    return render_template("favorites.html", items=items)


@app.route("/delete_favorite/<int:item_id>")
def delete_favorite(item_id):
    con = get_db()
    cur = con.cursor()
    cur.execute("DELETE FROM favorites WHERE id = ?", (item_id,))
    con.commit()
    con.close()

    return redirect(url_for("favorites"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)