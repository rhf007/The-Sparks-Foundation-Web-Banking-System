from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.secret_key = '176td120_87y498ydgfh'

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///task.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")

#main page
@app.route("/home")
def home():

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

#View Customers
@app.route("/view")
def view():

    #Show customers DB
    customers = db.execute("SELECT * FROM customers")
    return render_template("view.html", customers=customers)

#Choose Customers to transfer money
@app.route("/transfer", methods=["POST","GET"])
def transfer():

    #Select customer
    custinfos = db.execute("SELECT * FROM customers")
    return render_template("transfer.html", custinfos=custinfos)

@app.route("/transfer2", methods=["POST","GET"])
def transfer2():

    customers = db.execute("SELECT * FROM customers")
    return render_template("transfer2.html",customers=customers)

#Transfer record
@app.route("/transfertable", methods=["GET","POST"])
def transfertable():

    customers = db.execute("SELECT * FROM customers")

    #Customer to transfer money from
    customer1 = request.form.get("fromcustomer")

    #Customer to transfer money to
    customer2 = request.form.get("tocustomer")

    #get Amount of money from page
    try:
        amount = int(request.form.get("amount"))
    except:
        return redirect("/home")

    #First customer balance
    usercash = db.execute("SELECT cash FROM customers WHERE name = ?",customer1)[0]["cash"]

    #Second customer balance
    usercash2 = db.execute("SELECT cash FROM customers WHERE name = ?",customer2)[0]["cash"]

    #Verifying input, if not verified, redirect to home page
    if not customer1 or not customer2 or not amount:
        return redirect("/home")
    elif customer1 == customer2:
        return redirect("/home")
    if amount > usercash:
        return redirect("/home")
    else:

        #Input verified, update both Customers' balance
        db.execute("UPDATE customers SET cash = ? WHERE name = ?", usercash-amount, customer1)
        db.execute("UPDATE customers SET cash = ? WHERE name = ?", usercash2+amount, customer2)

        #Update transfer record
        db.execute("INSERT INTO transfers (first_customer_name, second_customer_name, transfer_amount) VALUES (?,?,?)",
                       customer1, customer2, amount)

    #Transfer done, display transfer record
    transfers = db.execute("SELECT first_customer_name, second_customer_name, transfer_amount FROM transfers")

    return render_template("transfertable.html",customers=customers, transfers=transfers)

