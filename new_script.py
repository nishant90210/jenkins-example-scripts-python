import numpy as np
import sys
import requests
import concurrent.futures
import json
import hmac
import hashlib
import urllib
import os

# SET UP
membershipFileName = '/Users/nishant/my-jenkins/jenkins-home/workspace/TestCSV/file/memberships.csv'

#System param
# env = ${env}
env = os.getenv("env")

#setting params
if (env == 'qa') :
    bookingApiHost = 'http://booking-engine.sticky.service.gcp01.edo.sv/engine'
    getBookingService = '/booking/v15/booking/'
    searchBookingService = '/bookingSearch/v1/searchBookings'
    searchBookingPwd = ''
    user = ''
    pwd_secret = ''
    membershipHostAndService = 'http://lb.membership.gke-apps.edo.sv/membership/search/v1/memberships/'
    recurringCollectionHostAndService = 'http://lb.recurring-collection.gke-apps.edo.sv/recurring-collection/'

elif (env == 'prod'):
    bookingApiHost = 'http://booking-engine.sticky.service.gcp01.edo.sv/engine'
    getBookingService = '/booking/v15/booking/'
    searchBookingService = '/bookingSearch/v1/searchBookings'
    searchBookingPwd = ''
    user = ''
    pwd_secret = ''
    membershipHostAndService = 'http://lb.membership.gke-apps.edo.sv/membership/search/v1/memberships/'
    recurringCollectionHostAndService = 'http://lb.recurring-collection.gke-apps.edo.sv/recurring-collection/recurring-collections/'

else:
    raise SystemExit("ERROR\nCorrect usage: \n[QA]     " + sys.argv[0] + " qa" + "\n[PROD]   " + sys.argv[0] + " prod")

#################################
##  PREPARE USER DATA WITH IDS ##
#################################

def prepare_data(inFileName):
# Load CSV train and test files
# Load CSV train and test files
    return np.loadtxt(open(inFileName, encoding='utf-8'), delimiter=",", skiprows=1, dtype=np.int64)

#################################
##  CALCULATE PWD BOOKING API  ##
#################################

def calculateHMAC(key, bookingId, locale):
    msg = str(str(bookingId).strip() + str(locale).strip())
    print("msg: " + msg)
    password = hmac.new(bytes(key, 'utf-8'), msg.encode('utf-8'), hashlib.sha1).hexdigest()
    print("The hmac password is : " +str(password))
    return password

################################
##      SEARCH MEMBERSHIP     ##
################################

def getMembership(membershipId):
    endpoint = membershipHostAndService + str(membershipId) + "?withMemberAccount=true"
    print(membershipId)
    headers = {
            'Content-Type': 'application/json;charset=UTF-8'
        }
    response = requests.get(url = endpoint, headers=headers)
    return {} if response.status_code == 204 else json.loads(response.text)

################################
##      EXPIRED MEMBERSHIP    ##
################################

def getExpiredMembership(website, userId):
    accountQuery = {
        "userId": str(userId)
    }
    query = {
        "status":"EXPIRED",
        "brand": getBrand(website),
        "memberAccountSearchRequest": accountQuery
    }
    endpoint = membershipHostAndService + "?search=" + str(query)
    headers = {
            'Content-Type': 'application/json;charset=UTF-8'
        }
    print(endpoint.replace("'", '"'))
    response = requests.get(url = endpoint.replace("'", '"'), headers=headers)
    return {} if response.status_code == 204 else json.loads(response.text)

################################
##      EXPIRED MEMBERSHIP    ##
################################

def getBrand(website):
    brand = "ED"
    if "OP" in website:
        brand = "OP"
    if "GO" in website:
        brand = "GV"
    return brand

################################
##  GET SUBSCRIPTION BOOKING  ##
################################

def getSubscriptionBooking(membershipId):
    endpoint = bookingApiHost + searchBookingService + ";user=membership;locale=es_ES"
    print(membershipId)
    payload = {
        "membershipId": str(membershipId),
        "isBookingSubscriptionPrime": True
    }
    print(payload)
    headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'password': searchBookingPwd
        }
    response = requests.post(url = endpoint, headers=headers, json = payload)
    return [] if response.status_code == 204 else json.loads(response.text)

################################
##   GET BUYER FROM  BOOKING  ##
################################

def getBookingBuyer(bookingId):
    endpoint = bookingApiHost + getBookingService + str(bookingId) + ";user=" + user + ";locale=es_ES"
    print(bookingId)
    hmac = calculateHMAC(pwd_secret, bookingId, "es_ES")
    headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'password': hmac
        }
    response = requests.get(url = endpoint, headers=headers)
    return [] if response.status_code == 204 else json.loads(response.text)

################################
##   GET BUYER FROM  BOOKING  ##
################################

def getBookingBuyer(bookingId):
    endpoint = bookingApiHost + getBookingService + str(bookingId) + ";user=" + user + ";locale=es_ES"
    print(bookingId)
    hmac = calculateHMAC(pwd_secret, bookingId, "es_ES")
    headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'password': hmac
        }
    response = requests.get(url = endpoint, headers=headers)
    return [] if response.status_code == 204 else json.loads(response.text)

################################
## RENEW RECURRING COLLECTION ##
################################

def renewRecurringCollection(recurringCollectionId, productId, buyer):
    endpoint = recurringCollectionHostAndService + str(recurringCollectionId) + "/renew"
    print(recurringCollectionId)
    payload = {
            "productId" : {
            "id" : str(productId),
            "type" : "MEMBERSHIP_RENEWAL"
        },
        "contactDetails" : {
            "name" : buyer["name"],
            "lastName" : buyer["lastNames"],
            "email" : buyer["mail"],
            "address" : buyer["address"],
            "cityName" : buyer["cityName"],
            "postcode" : buyer["zipCode"],
            "countryCode" : buyer["country"],
            "phoneNumber" : buyer["phoneNumber"]["number"]
        }
    }
    headers = {
            'Content-Type': 'application/json;charset=UTF-8'
        }
    print(payload)
    print(endpoint)
    response = requests.put(url = endpoint, headers=headers, json = payload)
    print(response.text)
    return [] if response.status_code == 204 else json.loads(response.text)
    #return payload

########################
##  RENEW MEMBERSHIP  ##
########################

def renewMembership(membershipId):
    membership = getMembership(membershipId)
    print(membership)
    website = membership['website']
    print(website)
    userId = membership['memberAccount']['userId']
    print(userId)
    oldMemberships = getExpiredMembership(website, userId)
    expiredMembershipId = oldMemberships[0]["id"]
    searchBookingResponse = getSubscriptionBooking(expiredMembershipId)
    bookings = searchBookingResponse['bookings']
    bookingId = bookings[0]['bookingBasicInfo']['id']
    bookingResponse = getBookingBuyer(bookingId)
    buyer = bookingResponse['buyer']
    print(buyer)
    result = renewRecurringCollection(membership["recurringCollectionId"], membershipId, buyer)
    print(result)


#####################################
##      RENEW ALL MEMBERSHIPS      ##
#####################################

def renewAllMemberships(membershipIds):
    for membershipId in membershipIds:
        print(membershipId)
        renewMembership(membershipId)
        print ("Processed entry # " + str(membershipId))
        print ("____________________________________")

#####################
## SCRIPT PROGRAM  ##
#####################

def program():
    # Preprocess file
    membershipsIds = prepare_data(membershipFileName)

    # Renewal Process
    renewAllMemberships(membershipsIds)

program()
print("Finished processing")
