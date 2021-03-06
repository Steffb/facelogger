__author__ = 'steffenfb'


import os
import re
import pickle
import datetime
import time
import hashlib
import operator


def localtest(userList, fromhour):

    #os.chdir('/Users/steffenfb/Documents/facelogs')

    logpath= 'facelogs'

    files =  os.listdir(logpath)
    files.pop(0)
    mydict={}



    #Adding users to the list
    for user in userList:
        mydict[user]=[]
    mydict['ref']=[]


    today  = datetime.datetime.fromtimestamp(time.time()).date()

    for file in files:

        try:
            filetime = re.search('\d+', file)
            filetime = datetime.datetime.fromtimestamp(int(file[filetime.start():filetime.end()]))
            #time[time.start():time.end()]
            fileDate =  filetime.date()
            filehour = filetime.time().hour
            #print 'this is filedate '+str(fileDate)
            #To create time reference
            #mydict['ref'].append(datetime.datetime.fromtimestamp(int(file[filetime.start():filetime.end()])).time())
            
        except:

            print str(filetime)+' could not find time '


        #Only add the files today
        if(fileDate == today and filehour > fromhour ):
        #if( filehour > 8 ):
            mydict['ref'].append(filetime.time())
            for user in userList:

                found = False
                data = pickle.load( open( logpath+'/'+file, "rb" ) )
                #Insert name here
                #hash = hashlib.md5('').hexdigest()
                hash =user
                for username in data:
                    if(hash in  username):
                        #print 'found on at '+str(time)
                        found = True
                        mydict[user].append(1)
                if(not found):
                    mydict[user].append(0)
                    #print '\t not active at '+str(time)

    return mydict

#Only return on last three hours
def last_x_hours(userList, backtrack_hours):

    logpath= 'facelogs'
    files =  os.listdir(logpath)
    files.pop(0)
    mydict={}

    #Adding users to the list
    for user in userList:
        mydict[user]=[]
    mydict['ref']=[]

    today  = datetime.datetime.fromtimestamp(time.time()).date()
    hournow = datetime.datetime.fromtimestamp(time.time()).hour
    for file in files:

        try:
            filetime = re.search('\d+', file)
            filetime = datetime.datetime.fromtimestamp(int(file[filetime.start():filetime.end()]))
            #time[time.start():time.end()]
            fileDate =  filetime.date()
            filehour = filetime.time().hour
            #print 'this is filedate '+str(fileDate)
            #To create time reference
            #mydict['ref'].append(datetime.datetime.fromtimestamp(int(file[filetime.start():filetime.end()])).time())

        except:

            print str(filetime)+' could not find time '


        #Only add the files today
        if(fileDate == today and (hournow-filehour) <= backtrack_hours ):
            mydict['ref'].append(filetime.time())
            for user in userList:

                found = False
                data = pickle.load( open( logpath+'/'+file, "rb" ) )
                #Insert name here
                #hash = hashlib.md5('').hexdigest()
                hash =user
                for username in data:

                    if(hash in  username):
                        #print 'found on at '+str(time)
                        found = True
                        mydict[user].append(1)

                if(not found):
                    mydict[user].append(0)
                    #print '\t not active at '+str(time)




    namelist = sort_on_most_active(mydict)
    return mydict,namelist


def sort_on_most_active(user_dict):
    count_dict = {}

    for key,value in user_dict.iteritems():
        total_counter = 0
        for element in value:
            if(element) : total_counter +=1

        count_dict[key] = total_counter

    count_dict =  sorted(count_dict.items(), key=operator.itemgetter(1))
    count_dict.reverse()
    sorted_name_list = []
    for i in count_dict:
        sorted_name_list.append(i[0])
    return sorted_name_list