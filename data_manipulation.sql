-- -----------------------------------------------------
-- Data Manipulation Queries 
-- -----------------------------------------------------
--SELECT FUNCTIONS
-- SELECT all items in a table
SELECT * FROM Cafes
SELECT * FROM Roasteries
SELECT * From Coffees
SELECT * FROM Invoices
SELECT * FROM Coffees_has_Invoices
-- get Names to populate the cafes list dropdown
SELECT cafe_name FROM Cafes
-- get all Coffee IDs and Names to populate the coffees list dropdown
SELECT offee_name FROM Coffees
-- get all Roastery Names to populate the roasteries list dropdown
SELECT roastery_name FROM Roasteries
-- get all Invoice IDs, cafe names, order dates, and invoice totals to populate the invoice list
SELECT invoice_id, (SELECT cafe_name FROM Cafes WHERE Cafes.cafe_id = Invoices.cafe_id) AS cafe_name, order_date, invoice_total FROM Invoices
-- get all Invoice IDs, cafe names and Coffee names for coffees that have invoices
SELECT 
	coffees_has_invoices_id, 
	(SELECT cafe_name FROM Cafes WHERE Cafes.cafe_id = 
 	(SELECT cafe_id FROM Invoices WHERE Invoices.invoice_id= 
  	(SELECT Invoices.invoice_id from Invoices WHERE Coffees_has_Invoices.invoice_id = Invoices.invoice_id))) AS Cafe_name, 
  	(SELECT coffee_name FROM Coffees WHERE Coffees.coffee_id = Coffees_has_Invoices.coffee_id) AS coffee_name 
  	FROM Coffees_has_Invoices

--SEARCH/FILTER FUNCTION

SELECT Roasteries.roastery_id, Coffees.coffee_name FROM Roasteries
    INNER JOIN Coffees ON coffees.roastery_id = (SELECT Roasteries.roastery_id WHERE Roasteries.roastery_name = :roastery_name_input)


-- INSERT FUNCTIONS
-- Insert new cafe
INSERT INTO Cafes (cafe_name, cafe_country, cafe_phone_number)
    VALUES (:cafe_name_input, :cafe_country_input, :cafe_phone_number_input)
-- Insert new invoice
INSERT INTO Invoices(cafe_id,order_date,invoice_total)
    VALUES ((SELECT cafe_id WHERE cafe_name = :cafe_name_input ), :order_date_input, :invoice_total_input)
-- Insert new Coffee
INSERT INTO Coffees (coffee_name, bean_type, roastery_id, retail_price, quantity_in_stock)
    VALUES (:coffee_name_input, :bean_type_input, (SELECT roastery_id WHERE roastery_name = :roastery_name_input), :retail_price_input, :quantity_in_stock_input)
-- Insert new Roastery
INSERT INTO Roasteries (roastery_name, roastery_country, roastery_phone, roastery_contact_person, contact_person_extension)
    VALUES (:roastery_name_input, :roastery_country_input, :roastery_phone_input, :roastery_contact_person_input, :contact_person_extension_input)
-- Associate a Coffee with an Invoice (M:M insertion)
INSERT INTO Coffees_has_Invoices(invoice_id, coffee_id)
    VALUES (:invoice_id_from_dropdown_input, (SELECT Coffees.coffee_id WHERE coffee_name =:coffee_name_from_dropdown_input))


--UPDATE FUNCTIONS
-- Update an invoice when a payment is made
UPDATE Invoices
    SET invoice_total = :invoice_total_input
    WHERE invoice_id = :invoice_id_selected_from_form
-- Update coffee information regarding quantity and price
UPDATE Coffees
    SET retail_price = :retail_price_input,
        quantity_in_stock = :quantity_in_stock_input
        WHERE (SELECT coffee_id WHERE coffee_name = coffee_name_selected_from_form)
-- Update cafe information
UPDATE Cafes
    SET cafe_name = :cafe_name_input
        cafe_country = :cafe_country_input
        cafe_phone_number = :cafe_phone_number_input
        WHERE (SELECT cafe_id WHERE cafe_name = :cafe_name_selected_from_form)
-- Update Roastery information
UPDATE Roasteries
    SET roastery_name = :roastery_name_input
        roastery_country = :roastery_country_input
        roastery_phone = :roastery_phone_input
        roastery_contact_person = :roastery_contact_person_input
        contact_person_extension - :contact_person_extension_input
        WHERE (SELECT roastery_id WHERE roastery_name = :roastery_name_selected_from_form)

-- DELETE FUNCTIONS
-- delete an coffee/invoice relationship (M:M relationship deletion)
DELETE FROM Coffees_has_Invoices 
    WHERE invoice_id= :invoice_id_selected_from_invoices_list 
    AND coffee_id = (SELECT coffee_id WHERE coffee_name = coffee_name_selected_from_form)
-- Delete a cafe
DELETE FROM Cafes
    WHERE cafe_id = (SELECT cafe_id WHERE cafe_name = :cafe_name_selected_from_form)
