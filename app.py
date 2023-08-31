# Citation for app structure
# Date 11/9/22
# Adapted Sample Flask application for a BSG database,
# Source URL https://github.com/osu-cs340-ecampus/flask-starter-app

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os


app = Flask(__name__)

# database connection
# Template:
# app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
# app.config["MYSQL_USER"] = "cs340_OSUusername"
# app.config["MYSQL_PASSWORD"] = "XXXX" | last 4 digits of OSU id
# app.config["MYSQL_DB"] = "cs340_OSUusername"
# app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# database connection info
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_crimina"
app.config["MYSQL_PASSWORD"] = "8759"
app.config["MYSQL_DB"] = "cs340_crimina"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Routes

@app.route("/")
def home():
    return render_template("home.j2")

############################## Cafes ############################## TODO: seperate these sections into different pages in the future

# route for cafes page
@app.route("/cafes", methods=["POST", "GET"])
def cafes():
    # Separate out the request methods, in this case this is for a POST
    # insert a cafe into the Cafes entity
    if request.method == "POST":
        # fire off if user presses the Add Cafes button
        if request.form.get("Add_Cafe"):
            # grab user form inputs
            cafe_name = request.form["cafe_name"]
            cafe_country = request.form["cafe_country"]
            cafe_phone_number = request.form["cafe_phone_number"]


            query = "INSERT INTO Cafes (cafe_name, cafe_country, cafe_phone_number) VALUES (%s, %s,%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (cafe_name, cafe_country, cafe_phone_number))
            mysql.connection.commit()

            # redirect back to cafe page
            return redirect("/cafes")

    # Grab Cafes data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the cafes in Cafes
        query = "SELECT * FROM Cafes"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("cafes.j2", data=data)

# route for delete functionality, deleting a cafe from Cafes,
# we want to pass the 'id' value of that cafe on button click (see HTML) via the route
@app.route("/delete_cafe/<int:id>")
def delete_cafe(id):
    # mySQL query to delete the cafe with our passed id
    query = "DELETE FROM Cafes WHERE cafe_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to cafes page
    return redirect("/cafes")


# route for edit functionality, updating the attributes of a cafe in Cafes
# similar to our delete route, we want to the pass the 'id' value of that cafe on button click (see HTML) via the route
@app.route("/edit_cafe/<int:id>", methods=["POST", "GET"])
def edit_cafes(id):
    if request.method == "GET":
        # mySQL query to grab the info of the cafe with our passed id
        query = "SELECT * FROM Cafes WHERE cafe_id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_cafe page passing our query data to the edit_cafe template
        return render_template("edit_cafe.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Cafe' button
        if request.form.get("Edit_Cafe"):
            # grab user form inputs
            cafe_id = request.form["cafe_id"]
            cafe_name = request.form["cafe_name"]
            cafe_country = request.form["cafe_country"]
            cafe_phone_number = request.form["cafe_phone_number"]

            query = "UPDATE Cafes SET Cafes.cafe_name = %s, Cafes.cafe_country = %s, Cafes.cafe_phone_number = %s WHERE Cafes.cafe_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (cafe_name, cafe_country, cafe_phone_number, cafe_id))
            mysql.connection.commit()

            # redirect back to cafes page after we execute the update query
            return redirect("/cafes")

############################## Roasteries ##############################

# route for roasteries page
@app.route("/roasteries", methods=["POST", "GET"])
def roasteries():
    # Separate out the request methods, in this case this is for a POST
    # insert a roastery into the Roasteries entity
    if request.method == "POST":
        # fire off if user presses the Add Roastery button
        if request.form.get("Add_Roastery"):
            # grab user form inputs
            roastery_name = request.form["roastery_name"]
            roastery_country = request.form["roastery_country"]
            roastery_phone = request.form["roastery_phone"]
            roastery_contact_person = request.form["roastery_contact_person"]
            contact_person_extension = request.form["contact_person_extension"]


            query = "INSERT INTO Roasteries (roastery_name, roastery_country, roastery_phone, roastery_contact_person, contact_person_extension ) VALUES (%s,%s,%s,%s,%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (roastery_name, roastery_country, roastery_phone, roastery_contact_person, contact_person_extension))
            mysql.connection.commit()

            # redirect back to roastery page
            return redirect("/roasteries")

    # Grab Roasteries data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the roasteries in Roasteries
        query = "SELECT * FROM Roasteries"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT roastery_id, roastery_name FROM Roasteries"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        roastery_data = cur.fetchall()

        return render_template("roasteries.j2", data=data, roasteries=roastery_data)

# route for delete functionality, deleting a roastery from Roasteries,
# we want to pass the 'id' value of that roastery on button click (see HTML) via the route
@app.route("/delete_roastery/<int:id>")
def delete_roastery(id):
    # mySQL query to delete the roastery with our passed id
    query = "DELETE FROM Roasteries WHERE roastery_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to roasteries page
    return redirect("/roasteries")


# route for edit functionality, updating the attributes of a roastery in Roasteries
# similar to our delete route, we want to the pass the 'id' value of that roastery on button click (see HTML) via the route
@app.route("/edit_roastery/<int:id>", methods=["POST", "GET"])
def edit_roasteries(id):
    if request.method == "GET":
        # mySQL query to grab the info of the roastery with our passed id
        query = "SELECT * FROM Roasteries WHERE roastery_id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_roastery page passing our query data to the edit_roastery template
        return render_template("edit_roastery.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Roastery' button
        if request.form.get("Edit_Roastery"):
            # grab user form inputs
            roastery_id = request.form["roastery_id"]
            roastery_name = request.form["roastery_name"]
            roastery_country = request.form["roastery_country"]
            roastery_phone = request.form["roastery_phone"]
            roastery_contact_person = request.form["roastery_contact_person"]
            contact_person_extension = request.form["contact_person_extension"]

            query = "UPDATE Roasteries SET Roasteries.roastery_name = %s, Roasteries.roastery_country = %s, Roasteries.roastery_phone = %s, Roasteries.roastery_contact_person = %s, Roasteries.contact_person_extension = %s WHERE Roasteries.roastery_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (roastery_name, roastery_country, roastery_phone, roastery_contact_person, contact_person_extension, roastery_id))
            mysql.connection.commit()

            # redirect back to roasteries page after we execute the update query
            return redirect("/roasteries")

@app.route("/search_roastery", methods=["GET"])
def search_roastery():
    if request.method == "GET":
        roastery_id = request.args.get("roastery_id")
        # mySQL query to grab the info of the coffees with our passed id
        query = "SELECT * FROM Coffees WHERE Coffees.roastery_id = %s" % (roastery_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        # render search_roastery page passing our query data to the search_roastery template
        return render_template("search.j2", data=data)

############################## Coffees ##############################
# route for coffees page
@app.route("/coffees", methods=["POST", "GET"])
def coffees():
    # Separate out the request methods, in this case this is for a POST
    # insert a coffee into the Coffees entity
    if request.method == "POST":
        # fire off if user presses the Add Coffees button
        if request.form.get("Add_Coffee"):
            # grab user form inputs
            coffee_name = request.form["coffee_name"]
            bean_type = request.form["bean_type"]
            roastery_id = request.form["roastery_id"]
            retail_price = request.form["retail_price"]
            quantity_in_stock = request.form["quantity_in_stock"]
            
             # account for null roastery ID AND null quantity in stock 
            if roastery_id == "" and quantity_in_stock == "":
                query = "INSERT INTO Coffees(coffee_name, bean_type, retail_price) VALUES (%s,%s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (coffee_name, bean_type, retail_price))
                mysql.connection.commit()

            # account for null roastery ID
            elif roastery_id == "":
                query = "INSERT INTO Coffees(coffee_name, bean_type, retail_price, quantity_in_stock) VALUES (%s,%s,%s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (coffee_name, bean_type, retail_price, quantity_in_stock))
                mysql.connection.commit()

            # account for null roastery ID
            elif quantity_in_stock == "":
                query = "INSERT INTO Coffees(coffee_name, bean_type, roastery_id, retail_price) VALUES (%s,%s,%s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (coffee_name, bean_type, roastery_id, retail_price))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Coffees(coffee_name, bean_type, roastery_id, retail_price, quantity_in_stock) VALUES (%s,%s,%s,%s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (coffee_name, bean_type, roastery_id, retail_price, quantity_in_stock))
                mysql.connection.commit()

            # redirect back to coffees page
            return redirect("/coffees")

    # Grab Coffees data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the coffees in Coffees
        query = "SELECT * FROM Coffees"
        # query = "SELECT Coffees.coffee_id, coffee_name, bean_type, Roasteries.roastery_name AS roastery_id, retail_price, quantity_in_stock FROM Coffees LEFT JOIN Roasteries ON roastery_id = Roasteries.id"
        # query = "SELECT Coffees.coffee_id, Coffees.coffee_name, Coffees.coffee_name, Roasteries.roastery_id AS roastery_id, Coffees.retail_price, Coffees.quantity_in_stock FROM Coffees LEFT JOIN Roasteries ON roastery_id = Roasteries.roastery_id"
        # query = "SELECT Coffees.coffee_id, coffee_name, coffee_name, Roasteries.roastery_name AS roastery, retail_price, quantity_in_stock FROM Coffees LEFT JOIN Roasteries ON roastery = Roasteries.roastery_id"

        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

    # mySQL query to grab roastery id/name data for our dropdown
        query2 = "SELECT roastery_id, roastery_name FROM Roasteries"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        roastery_data = cur.fetchall()

        return render_template("coffees.j2", data=data, roasteries=roastery_data)

# route for delete functionality, deleting a coffee from Coffees,
# we want to pass the 'id' value of that coffee on button click (see HTML) via the route
@app.route("/delete_coffee/<int:id>")
def delete_coffee(id):
    # mySQL query to delete the coffee with our passed id
    query = "DELETE FROM Coffees WHERE coffee_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to coffees page
    return redirect("/coffees")


# route for edit functionality, updating the attributes of a coffee in Coffees
# similar to our delete route, we want to the pass the 'id' value of that coffee on button click (see HTML) via the route
@app.route("/edit_coffee/<int:id>", methods=["POST", "GET"])
def edit_coffee(id):
    if request.method == "GET":
        # mySQL query to grab the info of the coffee with our passed id
        query = "SELECT * FROM Coffees WHERE coffee_id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab roastery id/name data for our dropdown
        query2 = "SELECT roastery_id, roastery_name FROM Roasteries"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        roastery_data = cur.fetchall()

        # render edit_coffee page passing our query data to the edit_coffee template
        return render_template("edit_coffee.j2", data=data, roasteries=roastery_data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Coffee' button
        if request.form.get("Edit_Coffee"):
            # grab user form inputs
            coffee_id = request.form["coffee_id"]
            coffee_name = request.form["coffee_name"]
            bean_type = request.form["bean_type"]
            roastery_id = request.form["roastery_id"]
            retail_price = request.form["retail_price"]
            quantity_in_stock = request.form["quantity_in_stock"]
            # account for null roastery id
            if roastery_id == "":
                query = "UPDATE Coffees SET Coffees.coffee_name = %s, Coffees.bean_type = %s, Coffees.roastery_id = Null, Coffees.retail_price = %s, Coffees.quantity_in_stock = %s WHERE Coffees.coffee_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (coffee_name, bean_type, retail_price, quantity_in_stock, coffee_id))
                mysql.connection.commit()

            # No null inputs
            else:
                query = "UPDATE Coffees SET Coffees.coffee_name = %s, Coffees.bean_type = %s, Coffees.roastery_id = %s, Coffees.retail_price = %s, Coffees.quantity_in_stock = %s WHERE Coffees.coffee_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (coffee_name, bean_type, roastery_id, retail_price, quantity_in_stock, coffee_id))
                mysql.connection.commit()

            # redirect back to coffees page after we execute the update query
            return redirect("/coffees")

############################## Invoices ##############################
# route for invoices page
@app.route("/invoices", methods=["POST", "GET"])
def invoices():
    # Separate out the request methods, in this case this is for a POST
    # insert a invoice into the Invoices entity
    if request.method == "POST":
        # fire off if user presses the Add Invoices button
        if request.form.get("Add_Invoice"):
            # grab user form inputs
            # invoice_id = request.form["invoice_id"]
            cafe_id = request.form["cafe_id"]
            order_date = request.form["order_date"]
            invoice_total = request.form["invoice_total"]



            query = "INSERT INTO Invoices (cafe_id, order_date, invoice_total) VALUES (%s,%s,%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, ( cafe_id, order_date, invoice_total))
            mysql.connection.commit()

            # redirect back to invoices page
            return redirect("/invoices")

    # Grab Invoices data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the invoices in Invoices
        query = "SELECT * FROM Invoices"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT cafe_id, cafe_name FROM Cafes"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        cafe_data = cur.fetchall()

        return render_template("invoices.j2", data=data, cafes=cafe_data)

# route for delete functionality, deleting a invoice from Invoices,
# we want to pass the 'id' value of that invoice on button click (see HTML) via the route
@app.route("/delete_invoice/<int:id>")
def delete_invoice(id):
    # mySQL query to delete the invoice with our passed id
    query = "DELETE FROM Invoices WHERE invoice_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to invoice page
    return redirect("/invoices")


# route for edit functionality, updating the attributes of a invoice in Invoices
# similar to our delete route, we want to the pass the 'id' value of that invoice on button click (see HTML) via the route
@app.route("/edit_invoice/<int:id>", methods=["POST", "GET"])
def edit_invoice(id):
    if request.method == "GET":
        # mySQL query to grab the info of the invoice with our passed id
        query = "SELECT * FROM Invoices WHERE invoice_id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT cafe_id, cafe_name FROM Cafes"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        cafe_data = cur.fetchall()

        # render edit_invoice page passing our query data to the edit_invoice template
        return render_template("edit_invoice.j2", data=data, cafes=cafe_data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Invoice' button
        if request.form.get("Edit_Invoice"):
            # grab user form inputs
            invoice_id = request.form["invoice_id"]
            cafe_id = request.form["cafe_id"]
            order_date = request.form["order_date"]
            invoice_total = request.form["invoice_total"]

            query = "UPDATE Invoices SET Invoices.cafe_id = %s, Invoices.order_date = %s, Invoices.invoice_total = %s WHERE Invoices.invoice_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (cafe_id, order_date, invoice_total, invoice_id))
            mysql.connection.commit()

            # redirect back to invoices page after we execute the update query
            return redirect("/invoices")

############################## Coffees/Invoices  ##############################
# route for Coffees_has_invoices page
@app.route("/CoffeesHasInvoices", methods=["POST", "GET"])
def coffees_has_invoices():
    # Separate out the request methods, in this case this is for a POST
    # insert a invoice into the Coffees/Invoices entity
    if request.method == "POST":
        # fire off if user presses the Add Invoices button
        if request.form.get("Add_Coffee_has_Invoice"):
            # grab user form inputs
            coffee_id = request.form["coffee_id"]
            invoice_id = request.form["invoice_id"]



            query = "INSERT INTO Coffees_has_Invoices (coffee_id, invoice_id) VALUES (%s,%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (coffee_id, invoice_id))
            mysql.connection.commit()

            # redirect back to Coffees/Invoices page
            return redirect("/CoffeesHasInvoices")

    # Grab Invoices data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the items in the intersection table
        query = "SELECT * FROM Coffees_has_Invoices"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT coffee_id, coffee_name FROM Coffees"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        coffee_data = cur.fetchall()

        query3 = "SELECT invoice_id FROM Invoices"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        invoice_data = cur.fetchall()


        return render_template("coffees_has_invoices.j2", data=data, coffees=coffee_data, invoices=invoice_data)

# route for delete functionality, deleting a invoice from Invoices,
# we want to pass the 'id' value of that invoice on button click (see HTML) via the route
@app.route("/delete_CoffeesHasInvoices/<int:id>")
def delete_coffees_has_invoices(id):
    # mySQL query to delete the invoice with our passed id
    query = "DELETE FROM Coffees_has_Invoices WHERE coffees_has_invoices_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to invoice page
    return redirect("/CoffeesHasInvoices")


# route for edit functionality, updating the attributes of a invoice in Invoices
# similar to our delete route, we want to the pass the 'id' value of that invoice on button click (see HTML) via the route
@app.route("/edit_CoffeesHasInvoices/<int:id>", methods=["POST", "GET"])
def edit_coffees_has_invoices(id):
    if request.method == "GET":
        # mySQL query to grab the info of the invoice with our passed id
        query = "SELECT * FROM Coffees_has_Invoices WHERE coffees_has_invoices_id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_invoice page passing our query data to the edit_invoice template
        return render_template("edit_coffees_has_invoices.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Invoice' button
        if request.form.get("edit_CoffeesHasInvoices"):
            # grab user form inputs
            coffees_has_invoices_id = request.form["coffees_has_invoices_id"]
            coffee_id = request.form["coffee_id"]
            invoice_id = request.form["invoice_id"]

            query = "UPDATE Coffees_has_Invoices SET Coffees_has_Invoices.coffee_id = %s, Coffees_has_Invoices.invoice_id = %s WHERE Coffees_has_Invoices.coffees_has_invoices_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (coffee_id, invoice_id, coffees_has_invoices_id))
            mysql.connection.commit()

            # redirect back to invoices page after we execute the update query
            return redirect("/CoffeesHasInvoices")

# Listener
# change the port number if deploying on the flip servers
if __name__ == "__main__":
    app.run(port=9113, debug=True)
