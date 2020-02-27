import requests
import csv
import sqlite3

# Importieren von Python Programmier Bibilotheken siehe https://de.wikipedia.org/wiki/Programmbibliothek
headers = {
    "accept": "application/json; charset=utf-8",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-length": "0",
    "content-type": "application/json; charset=utf-8",
    # "cookie: seastate"= "TGFzdFNlYXJjaA==:ZmFsc2UsMTU3NTYzNTc3NzEzOCwvcmFkaXVzL3dvaG51bmctbWlldGVuP2NlbnRlcm9mc2VhcmNoYWRkcmVzcz1CZXJsaW47MTA4Mjk7Ozs7Jmdlb2Nvb3JkaW5hdGVzPTUyLjQ4NTY7MTMuMzY0OTU7NS4w"; feature_ab_tests="ADS2042=ON"; ABNTEST=1573865718; S24UT=S24UT%7C509043f8-8c09-45b9-bcca-a8c40db9bd08; longUnreliableState="dWlkcg==:YS0wMTZlNzFiNTAzMzkwMDUyOGM5ZjU1N2IwNjM4MDMwNzIwMDIxMDZhMDBiZDA="; CONSENTMGR=consent:true%7Cts:1575635791724; utag_main=v_id:016e71b5033900528c9f557b063803072002106a00bd0$_sn:9$_ss:0$_st:1575637591726$psn_usr_login_cookie:False%3Bexp-1605401718702$faktorio:true$dc_visit:9$ses_id:1575635398336%3Bexp-session$_pn:7%3Bexp-session$referrer_to_lp:%3Bexp-session$dc_event:23%3Bexp-session$survey_overlay:b%3Bexp-session,
    "origin": "https://www.immobilienscout24.de",
    "referer": "https://www.immobilienscout24.de/Suche/radius/wohnung-mieten?centerofsearchaddress=Berlin;10829;;;;&geocoordinates=52.4856;13.36495;5.0&enteredFrom=one_step_search",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}


searchresults = []
pageexists = True
i = 1
while pageexists:
    try:
        r = requests.post(
            f"https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-mieten?pagenumber={i}",
            headers=headers,
        )
        rdict = r.json()
        try:
            searchresults.append(
                rdict["searchResponseModel"]["resultlist.resultlist"][
                    "resultlistEntries"
                ][0]["resultlistEntry"]
            )
        except:
            print("end of sites")
            pageexists = False
    except:
        print("end of sites")
        pageexists = False
    i += 1


conn = sqlite3.connect("wohnungen.db")
c = conn.cursor()
for d in searchresults:
    for x in d:
        wohnung = {
            "id": x["@id"],
            "title": x["resultlist.realEstate"]["title"],
            "postcode": x["resultlist.realEstate"]["address"]["postcode"],
            "price": x["resultlist.realEstate"]["price"]["value"],
        }
        c.execute(
            f"""INSERT INTO Wohnung VALUES (?,?,?,?)""",
            (wohnung["id"], wohnung["title"], wohnung["postcode"], wohnung["price"],),
        )
        conn.commit()
conn.close()

