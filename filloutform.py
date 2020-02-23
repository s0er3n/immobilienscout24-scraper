import requests
from requests_html import HTMLSession
import sqlite3
from sqlite3 import Error
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
)


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


def select_all_flats(conn):
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


def main():
    database = r"wohnungen.db"

    # create a database connection
    conn = create_connection(database)
    cur = conn.cursor()
    driver = webdriver.Chrome("/home/soeren/immobilienscout24-scraper/chromedriver")
    with conn:
        session = HTMLSession()
        for row in select_all_flats(conn):
            url = (
                f"https://www.immobilienscout24.de/expose/{row[0]}#/basicContact/email"
            )
            while True:
                try:
                    driver.get(url)
                    break
                except:
                    print("Error")
                    time.sleep(5)


            anfragekanngesendetwerden = "Anfrage senden" in driver.page_source
            if anfragekanngesendetwerden:
                print("FUNKTIONIERT")
                cur.execute(f"UPDATE Wohnung SET useable = 1 WHERE id = {row[0]};")
            else:
                print("FUNKTIONIERT NICHT")
                cur.execute(f"UPDATE Wohnung SET useable = 0 WHERE id = {row[0]};")
            conn.commit()


if __name__ == "__main__":
    main()

