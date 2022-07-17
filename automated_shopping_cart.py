############################### Import Library ###############################

import cv2
import drivers
from pyzbar.pyzbar import decode
import sqlite3
from time import sleep

############################### Create Connection ###############################

shop_database = sqlite3.connect("shop_database.db")
shop_cursor = shop_database.cursor()

############################### Scan and decode barcode ###############################


def decode_barcode():
    try:
        vid = cv2.VideoCapture("http://asd:123@192.168.0.111:8080/video")
        # vid = cv2.VideoCapture(0)
        while True:
            ret, frame = vid.read()
            cv2.imshow("frame", frame)
            k = cv2.waitKey(1)
            if k == ord("r"):
                print("Removing")
                detectedBarcodes = decode(frame)
                flag = 0
                print("Flag:", flag)
                for barcode in detectedBarcodes:
                    print("Barcode Data:", barcode.data)
                return int(barcode.data), flag
            if k == ord("c"):
                print("Captured")
                flag = 1
                print("Flag: ", flag)
                detectedBarcodes = decode(frame)
                for barcode in detectedBarcodes:
                    print("Barcode Data:", barcode.data)
                return int(barcode.data), flag
            if k == ord("q"):
                break
    except Exception as e:
        pass


############################### Update Cart ###############################


def updateCart(product_details, flag):

    try:
        total_amount = float(product_details[0][3])
        item = """SELECT EXISTS(SELECT 1 FROM purchased WHERE name = ?)"""
        shop_cursor.execute(item, (product_details[0][1],))
        cart_items = shop_cursor.fetchall()
        print("In update FLAG = ", flag)
        if cart_items[0][0] == 1:
            if flag == 1:
                shop_cursor.execute(
                    "SELECT quantity FROM purchased WHERE name = ?",
                    (product_details[0][1],),
                )
                item_quantity = shop_cursor.fetchall()
                quantity = int(item_quantity[0][0]) + 1
                shop_cursor.execute(
                    "UPDATE purchased SET quantity = ? WHERE name = ?",
                    (quantity, product_details[0][1]),
                )
                price = float(product_details[0][3])
                total_amount = price * quantity
            elif flag == 0:
                shop_cursor.execute(
                    "SELECT quantity FROM purchased WHERE name = ?",
                    (product_details[0][1],),
                )
                item_quantity = shop_cursor.fetchall()
                quantity = int(item_quantity[0][0]) - 1
                shop_cursor.execute(
                    "UPDATE purchased SET quantity = ? WHERE name = ?",
                    (quantity, product_details[0][1]),
                )
                price = float(product_details[0][3])
                total_amount = price * quantity
                if total_amount < 0 or quantity < 0:
                    total_amount = 0
                    quantity = 0
                    shop_cursor.execute(
                        "DELETE FROM purchased WHERE name = ?", (product_details[0][1],)
                    )
        else:
            if flag == 1:
                print("Adding {0} to cart".format(product_details[0][1]))
                cart_list = (
                    """INSERT INTO purchased (name,price, quantity) VALUES (?,?,?)"""
                )
                shop_cursor.execute(
                    cart_list, (product_details[0][1], product_details[0][3], 1)
                )
                total_amount = float(product_details[0][3])
                shop_cursor.execute(
                    "UPDATE purchased SET total = ? WHERE name = ?",
                    (total_amount, product_details[0][1]),
                )
            elif flag == 0:
                pass

        shop_cursor.execute(
            "UPDATE purchased SET total = ? WHERE name = ?",
            (total_amount, product_details[0][1]),
        )

        shop_database.commit()

    except Exception as e:
        pass


############################### Display to LCD ###############################


def display(product_details):
    display = drivers.Lcd()
    try:
        for items in product_details:
            display.lcd_clear()
            display.lcd_display_string(
                str(items[0]), 1
            )  # Write line of text to first line of display
            display.lcd_display_string(
                "Price:" + str(items[1]), 2
            )  # Write line of text to second line of display
            sleep(0.5)
            display.lcd_display_string("Quantity:" + str(items[2]), 2)
            sleep(0.5)
            display.lcd_clear()
            sleep(0.5)
        display.lcd_display_string("Total Bill:", 1)
        display.lcd_display_string(str(total_amount), 2)
    except KeyboardInterrupt:
        print("Cleaning up!")
        display.lcd_clear()


############################### Add Scanned Barcode to cart ###############################


def add_to_cart():
    try:
        global total_amount
        total_amount = 0.0
        detectedBarcodes, flag = decode_barcode()
        product_details = """select * from product where code = ?"""
        shop_cursor.execute(product_details, (detectedBarcodes,))
        product_details = shop_cursor.fetchall()
        updateCart(product_details, flag)
        shop_cursor.execute("SELECT * FROM purchased")
        purchased_items = shop_cursor.fetchall()

        print("Items in Cart are:")

        print("###############################")

        total = """select total from purchased"""
        shop_cursor.execute(total)
        total = list(shop_cursor.fetchall())
        for i in range(len(total)):
            total_amount = total_amount + sum(list(total[i]))
        # display(purchased_items)
        for items in purchased_items:
            # print("items", items)
            print("Name: {0}, \t  Price: {1}".format(items[0], items[1]))
            # print("Price: ", items[1])
            print("Quantity: {0}, \t  Total: {1}".format(items[2], items[3]))
            print("----------------------------------------------------------------")

        print("Bill Total:", total_amount)
        print("###############################")

        print("\n")

    except Exception as e:
        pass


shop_cursor.execute("DELETE FROM purchased;",)

while True:
    add_to_cart()

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break

