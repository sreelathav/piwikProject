"""  Author: Sree Latha Vallabhaneni
     prepared and tested March - May 2015
     Python script: liveVisitorHTMLreport.py
     command to run eg: python liveVisitorHTMLreport.py 3 1
     Program to extract the live visitor data from Piwik analytics API
     The requirements are Piwik instance Url, the token auth of the user (with view permissions on the data)
     to be replaced by correct credentials within the script
     The idSite of the tracking Website (argument 1)
     and number of hours (argument 2) to indicate how many hours to run the script
     are to given as command line arguments"""
import sys
import urllib2
import json
import os
import time
import webbrowser
import subprocess
global idsite

def getWebsiteURL():
    
    url = "http://IP-ADDRESS/piwik/?module=API&method=SitesManager.getSiteUrlsFromId&idSite="+idsite+"&format=json&token_auth=1a228667ee054bbe4d17943145b7822b"
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    json_string = response.read()
    response.close()
    return json.loads(json_string)

def getLiveVisitorId():
    
    url = "http://IP-AD/piwik/?module=API&method=Live.getMostRecentVisitorId&idSite="+idsite+"&format=json&token_auth=1a228667ee054bbe4d17943145b7822b"
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    json_string = response.read()
    response.close()
    return json.loads(json_string)

def getVisitorProfile():
    
    visitorId = getLiveVisitorId()
    url = "http://IP-AD/piwik/?module=API&method=Live.getVisitorProfile&idSite="+idsite+"&VisitorId==visitorId&format=json&token_auth=1a228667ee054bbe4d17943145b7822b"
    
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    json_string = response.read()
    response.close()
    
    return visitorId, json_string
    
def displayLiveData():
    
    siteObject = getWebsiteURL()
    website = siteObject[0]

    visitorID, json_string_data = getVisitorProfile()
    
    presentData = json.loads(json_string_data)
    print presentData
    visitorId = visitorID.get("value")
    
    
    lastVisits = presentData.get("lastVisits")
    
    visiDateTime = lastVisits[0].get("serverDatePrettyFirstAction")+ " " + lastVisits[0].get("serverTimePretty")
    
    visitorIP = lastVisits[0].get("visitIp")
    visitType = lastVisits[0].get("visitorType")
    os = lastVisits[0].get("operatingSystemName")
    browser = lastVisits[0].get("browserName")
    referrer = lastVisits[0].get("referrerType")
    
    countries =  presentData.get("countries")
    country = countries[0].get("prettyName")
    totalVisits = presentData.get("totalVisits")
    numberActions = presentData.get("totalActions")
    timeSpent = presentData.get("totalVisitDurationPretty")
    
    localTime = time.asctime( time.localtime(time.time()) )
    print "Local current time :", localTime
    print "Website under monitoring: ", website
    print "Visitor ID: ", visitorId
    
    print "--------------------------------------------------------------------"
    print "             The profile of the live visitor "
    print "--------------------------------------------------------------------"
    print " "
    print "  Total number of visits: ", totalVisits
    print "  Number of Actions: ", numberActions
    print "  Total time spent on the site: ", timeSpent
    print "  The visit originated from the country: ", country
    print " "
    print "  Latest visit information:"
    print "  The visitor IP address: ", visitorIP 
    print "  The type of the visit: ",visitType 
    print "  The Operating system of the visitor: ", os
    print "  The browser used by the visitor: ", browser
    print "  The referrer of the visit: ",referrer
    print " "
    print "--------------------------------------------------------------------"

def displayHTMLreport():
    siteObject = getWebsiteURL()
    website = siteObject[0]

    visitorID, json_string_data = getVisitorProfile()
    
    presentData = json.loads(json_string_data)
    
    visitorId = visitorID.get("value")
    print "Visitor ID: ", visitorId
    #print presentData
    lastVisits = presentData.get("lastVisits")
    
    visiDateTime = lastVisits[0].get("serverDatePrettyFirstAction")+ " " + lastVisits[0].get("serverTimePretty")
    
    visitorIP = lastVisits[0].get("visitIp")
    visitType = lastVisits[0].get("visitorType")
    os = lastVisits[0].get("operatingSystemName")
    browser = lastVisits[0].get("browserName")
    referrer = lastVisits[0].get("referrerType")
    
    countries =  presentData.get("countries")
    country = countries[0].get("prettyName")
    totalVisits = presentData.get("totalVisits")
    numberActions = presentData.get("totalActions")
    timeSpent = presentData.get("totalVisitDurationPretty")
    
        
    f = open('liveVisitorData.html','w')
    localTime = time.asctime( time.localtime(time.time()) )
    print "Local current time :", localTime
    #
    #              HTML PAGE CREATION
    #
    messageHead = '''<html>
    <head><title>Sree Analytics Service</title></head>
    <head>Monitoring Website  ''' + str(website) + ''' </head>'''
    currentTime = '''<body><p>Local current time  ''' + str(localTime) 
    messageB0 = '''</p><p>*--------LIVE VISITOR PROFILE--------*'''
    messageB1 = '''</p><p>Visitor Id: ''' + str(visitorId)
    visitTime = '''</p><p>Visiting date time : ''' + str(visiDateTime)
    messageB2 = '''</p><p>Total number of visits: ''' + str(totalVisits)
    messageB3 = '''</p><p>Number of Actions: '''+ str(numberActions)
    messageB4 = '''</p><p>Total time spent on the site: '''+ str(timeSpent)
    messageB5 = '''</p><p>The visit is from country: '''+ str(country)
    messageB6 = '''</p><p>The visitor IP address: '''+ str(visitorIP)
    messageB7 = '''</p><p>The type of the visit: '''+ str(visitType)
    messageB8 = '''</p><p>The Operating system of the visitor: '''+ str(os)
    messageB9 = '''</p><p>The browser used by the visitor: '''+ str(browser)
    messageB10 = '''</p><p>The referrer of the visit: '''+ str(referrer)
    messageEND = '''</p><p>*-------------END REPORT--------------*</p></body></html>'''
    message = messageHead + currentTime + messageB0 + messageB1 + visitTime + messageB2 + messageB3 + messageB4 + messageB5 + messageB6 + messageB7 + messageB8 + messageB9 + messageB10 + messageEND
    f.write(message)
    f.close()
    if sys.platform == 'darwin':   
       subprocess.Popen(['open','liveVisitorData.html'])
    else:    
       webbrowser.open_new_tab('liveVisitorData.html')
    return visitorId   
     
def displayInstructions():
    print " "
    print "__________________________________________________"
    print "              General Instructions               "
    print "__________________________________________________"
    print " "
    print " The script tested on Python version 2.7.5 "
    print '''  Before running this script make sure you replace the '&token_auth' in the http request API calls
               with your own User authentication token. '''
    print ''' The user with the given token_auth should have 'view' permissions to access the database'''
    print '''  Also make sure the site id of the website you are requesting data, 'idSite' be correctly given in the request url.
               This value can be checked in the tracking code of the website under study. '''
    print " "
    
def main(siteId,numberOfHours):
    global idsite
    #displayInstructions()
    idsite=str(siteId)
    n = int(numberOfHours)*12
    liveVisitorId = displayHTMLreport()
    for i in range(n):
        time.sleep(30)
        currentVisitorId = getLiveVisitorId()
        if (liveVisitorId == currentVisitorId.get("value")):
            print "No new visitor"    
        else:
            liveVisitorId = displayHTMLreport()
            
    
if __name__ == "__main__":
   #Expects 2 parameters from command line 2 integers separated by blank. 
   #eg. idsite = 3 and number of hours = 1
   #print sys.argv[1]
   #print sys.argv[2]
   main(sys.argv[1],sys.argv[2])

   
    



