import sqlite3

################################ Create Connection ################################

connection = sqlite3.connect("shop_database.db")
cursor = connection.cursor()

################################ Create a new database ################################

# cursor.execute(
#     """CREATE TABLE IF NOT EXISTS purchased (name varchar(255), price float,quantity int default 1, total float default 0.00)"""
# )
# cursor.execute(
#     """CREATE TABLE IF NOT EXISTS product (id int, name varchar(255), code varchar(255),price float)"""
# )


################################ Insert Values to Database ################################

# cursor.execute(
#     """INSERT INTO product (id,name,code,price) VALUES (1, 'Cello Arrow Gel', '8907234501469', 6.00)"""
# )
# cursor.execute(
#     """INSERT INTO product (id,name,code,price) VALUES (2, 'Seagate Harddisk', '7636490063428', 5599.00)"""
# )
# cursor.execute(
#     """INSERT INTO product (id,name,code,price) VALUES (3, 'Classmate Notebook', '8902519009425', 33.00)"""
# )
# cursor.execute(
#     """INSERT INTO product (id,name,code,price) VALUES (4, 'Britannia Bourbon Biscuit', '8901063030022', 10.00)"""
# )
# cursor.execute(
#     """INSERT INTO product (id,name,code,price) VALUES (5, 'Gone Mad Choco Pillow', '8906065450069', 10.00)"""
# )
# cursor.execute(
#     """INSERT INTO product (id,name,code,price) VALUES (6, 'Sting', '8902080000227', 20.00)"""
# )
# cursor.execute(
#     """INSERT INTO purchased (name,price, quantity) VALUES ('Cello Arrow Gel', 6.00,1)"""
# )

################################ Update Values ################################

# cursor.execute("""Update product set id = 6 where code = 8902080000227""")

################################ Delete Values from Database ################################

# cursor.execute("""DELETE FROM prodect WHERE barcode = xxxxxx""")
cursor.execute("DELETE FROM purchased;",)

################################ Display All Values in Database ################################

cursor.execute("SELECT * FROM purchased")
records = cursor.fetchall()
print("Total rows are:  ", len(records))
print("Printing each row")
for row in records:
    print("Id: ", row[0])
    print("Name: ", row[1])
    print("Barcode: ", row[2])
    print("Total: ", row[3])
    print("\n")

################################ Close Connection ################################

connection.commit()
connection.close()

################################ END ###############################################


# cursor.execute(
#     """INSERT INTO product (name,price,quantity) VALUES (items[bar_label_value]["Name"],
#     items[bar_label_value]["Price"],
#     items[bar_label_value]["Quantity"],)"""
# )

