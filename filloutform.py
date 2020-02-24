import sqlite3
from sqlite3 import Error
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time




def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_all_flats_without_useability_value(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return: rows
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Wohnung WHERE useable is NULL")

    rows = cur.fetchall()

    for row in rows:
        print(row)

    return rows

def select_useable_flats(conn):
    """
    returns rows with useable flats
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Wohnung WHERE useable is 1")

    rows = cur.fetchall()

    for row in rows:
        print(row)

    return rows


def find_useable_flats():
    database = r"wohnungen.db"

    # create a database connection
    conn = create_connection(database)
    cur = conn.cursor()
    driver = webdriver.Chrome()
    with conn:
        for row in select_all_flats_without_useability_value(conn):
            url = (
                f"https://www.immobilienscout24.de/expose/{row[0]}#/basicContact/email"
            )
            while True:
                try:
                    driver.get(url)
                    time.sleep(1)
                    break
                except:
                    print("Error")
                    driver.quit()
                    driver = webdriver.Chrome()
                    time.sleep(5)


            anfragekanngesendetwerden = "Anfrage senden" in driver.page_source
            if anfragekanngesendetwerden:
                print("FUNKTIONIERT")
                cur.execute(f"UPDATE Wohnung SET useable = 1 WHERE id = {row[0]};")
            else:
                print("FUNKTIONIERT NICHT")
                cur.execute(f"UPDATE Wohnung SET useable = 0 WHERE id = {row[0]};")
            conn.commit()


def fill_out_form(driver, url, gender, message, firstname, lastname, email, phonenumber, streetname, housenumber, postcode, city):
    profile = [message, firstname, lastname, email, phonenumber, streetname, housenumber, postcode, city]
    driver.get(url)
    time.sleep(2)
    ids = ["contactForm-Message","contactForm-firstName","contactForm-lastName","contactForm-emailAddress", "contactForm-phoneNumber","contactForm-street","contactForm-houseNumber", "contactForm-postcode","contactForm-city"]
    for id, text in zip(ids, profile):
        driver.find_element_by_id(id).clear()
        driver.find_element_by_id(id).send_keys(text)
    driver.find_element_by_xpath(f"//select[@id='contactForm-salutation']/option[text()='{gender}']").click()
    time.sleep(5)

if __name__ == "__main__":
    
    find_useable_flats()
    driver = webdriver.Chrome()
    fill_out_form(driver) # needs profiles


