__author__ = 'steffenfb'
import re
from bs4 import BeautifulSoup
import json

def cookieToOneLine():

    file = open('cookie.txt','r')

    content =  file.read()

    clean = content.replace('\n','')
    clean = content.replace('\"','\'')

    file = open('cookie.txt','w')
    file.write(clean)

    file.close()

testStr = 'for (;;); {"t":"fullReload","seq":80}'

def cleanStringToOnlyNumbersAndLetters(input):
    return re.sub('[^a-z0-9]','',input)

#cleanstring = cleanStringToOnlyNumbersAndLetters(testStr)




def getSeqNumber(input):
     cleanstring = cleanStringToOnlyNumbersAndLetters(input)
     cleanstring = cleanstring.split('seq')[1]
     res = re.search('\d{1,3}',cleanstring)
     #print 'found '+str(res.start())+' and '+str(res.end())
     return cleanstring[res.start():res.end()]

    #re.search('\d+',cleanstring).string




def htmlToJsonCleaner(html):

    soup = BeautifulSoup(html,'html.parser')

    page =  soup.body.pre.contents[0]
    if 'for (;;); ' in page:
        page = page[9:]
        print page

        jsonObj = json.loads(page)
        return jsonObj



#htmlToJsonCleaner(file('jsondump.json','r').read())
