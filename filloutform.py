import sqlite3
from sqlite3 import Error
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

yilmaz = ["Herr", """Sehr geehrte Damen und Herren,

mein Name ist Elias Yilmaz, ich bin 21 Jahre alt und suche eine Wohnung in Berlin. Ich bin ledig, arbeite seit kurzem als Social Media Manager und kann ein geregeltes Einkommen nachweisen. Die von Ihnen angebotene Wohnung entspricht genau meinen Vorstellungen. Über eine Rückmeldung von Ihnen und einen Besichtigungstermin würde ich mich deshalb sehr freuen. Bei der Terminfindung richte ich mich gerne ganz nach Ihren Wünschen.

Mit freundlichen Grüßen

Elias Yilmaz""" , "Elias", "Yilmaz", "elias.yilmaz98@protonmail.com", "", "Vogelsanger Str.", "196", "50825", "Köln" ]
mueller = ["Herr", """Sehr geehrte Damen und Herren,

mein Name ist Elias Müller, ich bin 21 Jahre alt und suche eine Wohnung in Berlin. Ich bin ledig, arbeite seit kurzem als Social Media Manager und kann ein geregeltes Einkommen nachweisen. Die von Ihnen angebotene Wohnung entspricht genau meinen Vorstellungen. Über eine Rückmeldung von Ihnen und einen Besichtigungstermin würde ich mich deshalb sehr freuen. Bei der Terminfindung richte ich mich gerne ganz nach Ihren Wünschen.

Mit freundlichen Grüßen

Elias Müller""" , "Elias", "Müller", "elias.mueller98@protonmail.com", "", "Vogelsanger Str.", "196", "50825", "Köln" ]


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
                    time.sleep(5)
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


def split_data(conn):
    cur = conn.cursor()

    for wohnungen in select_useable_flats(conn):
        import random
        cur.execute(f"UPDATE Wohnung SET profil = {random.randint(0,1)} WHERE id = {wohnungen[0]};")
    conn.commit()
if __name__ == "__main__":
    #driver = webdriver.Chrome()
    # fill_out_form(driver,"https://www.immobilienscout24.de/expose/115478066?referrer=RESULT_LIST_LISTING&navigationServiceUrl=%2FSuche%2Fcontroller%2FexposeNavigation%2Fnavigate.go%3FsearchUrl%3D%2FSuche%2Fde%2Fberlin%2Fberlin%2Fwohnung-mieten%3FenteredFrom%253Done_step_search%26exposeId%3D114618260&navigationHasNext=true&navigationBarType=RESULT_LIST&searchId=3881c980-7942-301c-9b68-f399848f6957&searchType=district#/basicContact/email", *yilmaz)
    
    split_data(create_connection(r"wohnungen.db"))
