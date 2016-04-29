from selenium import webdriver
import json
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time
import os
import pickle
import hashlib
import datetime



def scrapeFacebook():

    #os.chdir('/Users/steffenfb/PycharmProjects/zzzzz/')
    print '\t[Console] Starting fetcher'
    file = open('SECRETS.txt','r')
    email = file.readline().split('=')[1]
    pwd = file.readline().split('=')[1]


    driver = webdriver.Firefox()

    # Change default timeout and window size.
    driver.implicitly_wait(120)
    driver.set_window_size(1280,700)

    driver.get('https://www.facebook.com/')
    emailBox = driver.find_element_by_id('email')
    emailBox.send_keys(email)
    passwordBox = driver.find_element_by_id('pass')
    passwordBox.send_keys(pwd)
    driver.find_element_by_id('loginbutton').click()
    # To let the async menu load
    print '\tsleeping'
    time.sleep(5)
    print '\tWoke up'
    cono = driver.find_element_by_tag_name('body')
    cono = cono.text.encode('ascii','ignore')

    driver.close()
    return cono

def getContent():
    file = open('dump','r')
    return file.read()

 # Set the hours you want the fetcher to fetch military time
 # Sleepsecond is how long break between fetches
def runner(fromhour, tohour, sleepseconds):
    while(True):
        now = time.time()

        #only fetching between 0600 and 1900
        currentHour =datetime.datetime.fromtimestamp(now).hour
        currentMin =datetime.datetime.fromtimestamp(now).minute

        if(currentHour < fromhour  or currentHour > tohour):
        #if(True):

            # if its not time sleep for an hour.
            print '[realfetcher] time is '+str(currentHour)
            print '[realfetcher] not fetching'
            print '[realfetcher] sleeping one hour'
            time.sleep(3600)
        else:

            print '[realfetcher] time is %d : %d'%(currentHour,currentMin)

            print 'Console > Collecting online people'

            #data = getContent()
            data = scrapeFacebook()
            #os.chdir('/Users/steffenfb/Documents/facelogs')
            lines = data.split('\n')
            collectNames =False
            onlineNames= []
            skipnext = False
            for line in lines:
                if (skipnext):
                    skipnext=False
                    continue
                if('Chat with friends' in line):
                    #print line
                    collectNames= True
                    continue
                if('GROUP CONVERSATIONS' in  line):
                    collectNames= False

                if ('MORE FRIENDS' in line):
                    collectNames = True
                    continue

                # To remove time
                if(collectNames):

                    if(len(line)>4):

                        #onlineNames.append(hashlib.md5(line).hexdigest())
                        onlineNames.append(line)
                        #print line

                    #Assume its a time and we want to skip the next line
                    if(len(line)<4):
                        skipnext = True


            pickle.dump(onlineNames, open('facelogs/'+str(int(time.time()))+'.p','wb'))
            print 'Console > sleeping for %d seconds'%(sleepseconds)
            print 'collected '+str(len(onlineNames))

            #Wait between fetching
            time.sleep(sleepseconds)



#scrapeFacebook()
runner(fromhour=0, tohour=24, sleepseconds=15)
