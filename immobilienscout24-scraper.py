import requests
import csv

headers = {
"accept": "application/json; charset=utf-8",
"accept-encoding": "gzip, deflate, br",
"accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
"content-length": "0",
"content-type": "application/json; charset=utf-8",
#"cookie: seastate"= "TGFzdFNlYXJjaA==:ZmFsc2UsMTU3NTYzNTc3NzEzOCwvcmFkaXVzL3dvaG51bmctbWlldGVuP2NlbnRlcm9mc2VhcmNoYWRkcmVzcz1CZXJsaW47MTA4Mjk7Ozs7Jmdlb2Nvb3JkaW5hdGVzPTUyLjQ4NTY7MTMuMzY0OTU7NS4w"; feature_ab_tests="ADS2042=ON"; ABNTEST=1573865718; S24UT=S24UT%7C509043f8-8c09-45b9-bcca-a8c40db9bd08; longUnreliableState="dWlkcg==:YS0wMTZlNzFiNTAzMzkwMDUyOGM5ZjU1N2IwNjM4MDMwNzIwMDIxMDZhMDBiZDA="; CONSENTMGR=consent:true%7Cts:1575635791724; utag_main=v_id:016e71b5033900528c9f557b063803072002106a00bd0$_sn:9$_ss:0$_st:1575637591726$psn_usr_login_cookie:False%3Bexp-1605401718702$faktorio:true$dc_visit:9$ses_id:1575635398336%3Bexp-session$_pn:7%3Bexp-session$referrer_to_lp:%3Bexp-session$dc_event:23%3Bexp-session$survey_overlay:b%3Bexp-session,
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
        r = requests.post(f"https://www.immobilienscout24.de/Suche/de/wohnung-mieten?pagenumber={i}",headers = headers)
        rdict = r.json()
        try:
            searchresults.append(rdict["searchResponseModel"]["resultlist.resultlist"]["resultlistEntries"][0]["resultlistEntry"])
        except:
            print("Fehler!")
    except:
        print("end of sites")
        pageexists = False
    i += 1

with open("immmo.csv", "w", encoding="utf-8") as file:
    writer = csv.writer(file)
    for d in searchresults:
        for x in d:
            writer.writerow([x["@id"],x["resultlist.realEstate"]["title"], x["resultlist.realEstate"]["price"]["value"]])

# payload = {"showPrivacyPolicyAcceptanceCheckbox":true,"personalData":{"salutation":"","firstName":None,"lastName":None,"company":None,"phoneNumber":None,"emailAddress":None,"postcode":None,"city":None,"street":None,"houseNumber":None,"message":"","dataProtectionAlreadyAccepted":False,"buyReason":None,"moveInDateType":None,"moveInDate":None,"numberOfPersons":None,"petsInHousehold":None,"employmentRelationship":None,"income":None,"ownCapital":None,"hasPreapproval":None,"schufaInformationProvided":None,"applicationPackageCompleted":None,"lotAvailable":None,"numberOfRequiredWorkingPlaces":None,"plannedInvestment":None,"commercialUsage":None,"extendedPersonalData":{"numberOfPersons":None,"employmentRelationship":None,"income":None,"buyReason":None,"ownCapital":None,"plannedInvestment":None}},"captchaData":{"captchaId":"","userAnswer":""},"nonceToken":"MTU3NTYzODM4NjkxMzo4MWQ4ODMwOThjNzVhNjQwMzI3Mzk0NDIwMjViOGFhNWE1ZTY5Njg4ZjU3M2VjZDBiYjY1MzZjNTA4MGY1ZWMzOjExNDYzMzEyNSwwOjcwNmFiNDlkYzk3ZWI5MmViNTVhZGQ0Y2M4MGI3ODk0YTBjZTE1M2UwNzMxNGNkOWY0MWVlMmVjZDA3MGI1Mzg1NjgzMjFmMjFiMWFmYWM0YWMxNzc3NGQ2YzY3MWM5YmMwZGEzYjViYTViMTgwYzc0MWE4ZmU5YWZhYzc1ZTdl","sendButtonDelay":0,"suspiciousRequest":False,"sendUserProfile":False,"contactType":"contactlayer","contactTypeApply":False,"sendSolvencyCheck":False,"commercialProfileExists":False,"userProfileExists":False}

# class Person:
#     def __init__(self,message, salutation, firstName, lastName, street, houseNumber, postcode, city, emailAddress):
#         self.payload= {
#             "showPrivacyPolicyAcceptanceCheckbox": True,
#             "personalData":
#             {"salutation": salutation,
#             "firstName":firstName,
#             "lastName":lastName,
#             "company":None,
#             "phoneNumber":None,
#             "emailAddress":emailAddress,
#             "postcode":postcode,
#             "city":city,
#             "street":street,
#             "houseNumber":houseNumber,
#             "message":message,
#             "dataProtectionAlreadyAccepted":False,
#             "buyReason":None,
#             "moveInDateType":None,
#             "moveInDate":None,
#             "numberOfPersons":None,
#             "petsInHousehold":None,
#             "employmentRelationship":None,
#             "income":None,
#             "ownCapital":None,
#             "hasPreapproval":None,
#             "schufaInformationProvided":None,
#             "applicationPackageCompleted":None,
#             "lotAvailable":None,
#             "numberOfRequiredWorkingPlaces":None,
#             "plannedInvestment":None,
#             "commercialUsage":None,
#             "extendedPersonalData":{"numberOfPersons":None,"employmentRelationship":None,"income":None,"buyReason":None,"ownCapital":None,"plannedInvestment":None}},"captchaData":{"captchaId":"","userAnswer":""},"nonceToken":"MTU3NTYzODM4NjkxMzo4MWQ4ODMwOThjNzVhNjQwMzI3Mzk0NDIwMjViOGFhNWE1ZTY5Njg4ZjU3M2VjZDBiYjY1MzZjNTA4MGY1ZWMzOjExNDYzMzEyNSwwOjcwNmFiNDlkYzk3ZWI5MmViNTVhZGQ0Y2M4MGI3ODk0YTBjZTE1M2UwNzMxNGNkOWY0MWVlMmVjZDA3MGI1Mzg1NjgzMjFmMjFiMWFmYWM0YWMxNzc3NGQ2YzY3MWM5YmMwZGEzYjViYTViMTgwYzc0MWE4ZmU5YWZhYzc1ZTdl","sendButtonDelay":0,"suspiciousRequest":False,"sendUserProfile":False,"contactType":"contactlayer","contactTypeApply":False,"sendSolvencyCheck":False,"commercialProfileExists":False,"userProfileExists":False
#         }

# print(Person("TEST NICHT ANTWORTEN", "Frau", "Sophie","Müller", "teststraße","12","10182", "Berlin","Test@example.com").payload)

# posturl = "https://www.immobilienscout24.de/expose/112710749/validate"

# r = requests.post(posturl, data=Person("TEST NICHT ANTWORTEN", "Frau", "Sophie","Müller", "teststraße",12,10182, "Berlin","Test@example.com").payload)
# print(r,r.text)
