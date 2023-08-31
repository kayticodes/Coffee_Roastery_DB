SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

-- -----------------------------------------------------
-- Table `Cafes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Cafes (
  cafe_id INT NOT NULL AUTO_INCREMENT,
  cafe_name VARCHAR(45) NOT NULL,
  cafe_country VARCHAR(45) NOT NULL,
  cafe_phone_number VARCHAR(45) NOT NULL,
  PRIMARY KEY (cafe_id)
)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Invoices`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Invoices (
  invoice_id INT NOT NULL AUTO_INCREMENT,
  cafe_id INT NOT NULL COMMENT 'will be a forign key from the cafes entity ',
  order_date DATE NOT NULL,
  invoice_total DECIMAL(9, 2) NOT NULL,
  PRIMARY KEY (invoice_id),
  FOREIGN KEY (cafe_id) REFERENCES Cafes (cafe_id) 
    ON DELETE RESTRICT
 )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Roasteries`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Roasteries (
  roastery_id INT NOT NULL AUTO_INCREMENT,
  roastery_name VARCHAR(45) NOT NULL,
  roastery_country VARCHAR(45) NOT NULL,
  roastery_phone VARCHAR(45) NOT NULL,
  roastery_contact_person VARCHAR(45) NOT NULL,
  contact_person_extension VARCHAR(45) NOT NULL,
  PRIMARY KEY (roastery_id)
  )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Coffees`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Coffees (
  coffee_id INT NOT NULL AUTO_INCREMENT,
  coffee_name VARCHAR(45) NULL,
  bean_type VARCHAR(45) NOT NULL,
  roastery_id INT NULL,
  retail_price DECIMAL(9, 2) NOT NULL,
  quantity_in_stock INT,
  PRIMARY KEY (coffee_id),
  FOREIGN KEY (roastery_id) REFERENCES Roasteries (roastery_id)
    ON DELETE CASCADE
)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Coffees_has_Invoices`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Coffees_has_Invoices (
  coffees_has_invoices_id INT NOT NULL AUTO_INCREMENT,
  coffee_id INT NOT NULL,
  invoice_id INT NOT NULL,
  PRIMARY KEY (coffees_has_invoices_id),
  FOREIGN KEY (coffee_id) REFERENCES Coffees(coffee_id)
    ON DELETE CASCADE,
  FOREIGN KEY (invoice_id) REFERENCES Invoices(invoice_id)
    ON DELETE CASCADE
)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Sample Data Insertion
-- -----------------------------------------------------
INSERT INTO Cafes (
    cafe_name, 
    cafe_country, 
    cafe_phone_number
    ) 
    VALUES 
    ('Hot & Cold Joint', 'USA', '503-713-7761'), 
    ('Bean Me Up Bistro', 'USA', '503-416-1005'),
    ('Mug Shot Coffee Bar', 'USA', '503-289-8560'), 
    ('The Hive Coffee Bar', 'USA', '503-807-8622'); 

INSERT INTO Roasteries (
    roastery_name, 
    roastery_country, 
    roastery_phone, 
    roastery_contact_person, 
    contact_person_extension
    ) 
    VALUES 
    ('First Dawn Roastery', 'USA', '216-245-0257', 'Mark Stanley', '858'), 
    ('Aurora Roasting Co', 'USA', '561-206-5154', 'Linda Yates', '123'), 
    ('Pressing Matter Roastery', 'USA', '331-240-1255', 'Clint Jordan', '1545'),
    ('Güd Cup Roastery', 'USA', '732-290-9967', 'Meghan Marshall', '42');

INSERT INTO Coffees ( 
	coffee_name, 
	bean_type, 
	roastery_id, 
	retail_price, 
	quantity_in_stock
	) 
VALUES 
(
    'ethiopia yirgacheffe',
    'light',
    (SELECT roastery_id FROM Roasteries WHERE roastery_name = "Güd Cup Roastery"),
    20,
    14
), 
(   'Sumatra',
    'dark',
    (SELECT roastery_id FROM Roasteries WHERE roastery_name = "First Dawn Roastery"),
    15,
    12
),
(
    'Three Region Blend',
    'medium/light',
    (SELECT roastery_id FROM Roasteries WHERE roastery_name = "Aurora Roasting Co"),
    16,
    25
),
(
    'Bella Vista',
    'medium',
    (SELECT roastery_id FROM Roasteries WHERE roastery_name = "Pressing Matter Roastery"),
    18.99,
    13
);


INSERT INTO Invoices (
    cafe_id,
    order_date,
    invoice_total
)
VALUES 
(
    (SELECT cafe_id FROM Cafes WHERE cafe_name = "Hot & Cold Joint"),
    '2022-04-08',
    440
),
(
    (SELECT cafe_id FROM Cafes WHERE cafe_name = "Hot & Cold Joint"),
    '2022-10-20',
    246.87
),
(
    (SELECT cafe_id FROM Cafes WHERE cafe_name = "Bean Me Up Bistro"),
    '2022-07-17',
    128
),
(
    (SELECT cafe_id FROM Cafes WHERE cafe_name = "The Hive Coffee Bar"),
    '2022-01-01',
    60
);
INSERT INTO Coffees_has_Invoices (
    invoice_id,
    coffee_id
)

VALUES 
(
    (SELECT invoice_id FROM Invoices WHERE order_date = '2022-04-08'),
    (SELECT coffee_id FROM Coffees WHERE coffee_name = "ethiopia yirgacheffe")
),
(
    (SELECT invoice_id FROM Invoices WHERE order_date = '2022-10-20'),
    (SELECT coffee_id FROM Coffees WHERE coffee_name = "ethiopia yirgacheffe")
),
(
    (SELECT invoice_id FROM Invoices WHERE order_date = '2022-10-20'),
    (SELECT coffee_id FROM Coffees WHERE coffee_name = "Sumatra")
),
(
    (SELECT invoice_id FROM Invoices WHERE order_date = '2022-07-17'),
    (SELECT coffee_id FROM Coffees WHERE coffee_name = "ethiopia yirgacheffe")
),
(
    (SELECT invoice_id FROM Invoices WHERE order_date = '2022-01-01'),
    (SELECT coffee_id FROM Coffees WHERE coffee_name = "Bella Vista")
);


SET FOREIGN_KEY_CHECKS=1;
COMMIT;