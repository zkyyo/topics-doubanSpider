from urllib.request import urlopen
from urllib.parse import quote
from operator import itemgetter
from bs4 import BeautifulSoup
import re



def getTopics(topics):
    for topic in topics:
        responses = topic.parent.next_sibling.next_sibling.next_sibling.next_sibling.get_text()
        if responses == '':
            continue
        responses = int(responses) 
        if responses > 10:
            L = []
            L.append(responses)
            L.append(topic["title"])
            L.append(topic["href"])
            topicBag.append(L)


topicBag = []
index = 1
def getFirstPage(Url):
    global index
    print("<------------group %d------------>]" % index)
    index += 1
    print("waiting -->"+Url)

    try:
        html = urlopen(Url)
        bs0bj = BeautifulSoup(html, "lxml")
        topics =  bs0bj.find("table", {"class":"olt"}).findAll("a", href=re.compile("https://www.douban.com/group/topic/.*"))
        getTopics(topics)
        
        secondUrl = bs0bj.find("a", href=re.compile(".*start=50"))
        if secondUrl != None:
            return secondUrl["href"]
        else:
            return None
    except AttributeError:
        return



def getNextPage(Url, page):
    global pageBag
    print("waiting -->"+Url)

    try:
        html = urlopen(Url)
        bs0bj = BeautifulSoup(html, "lxml")
        topics =  bs0bj.find("table", {"class":"olt"}).findAll("a", href=re.compile("https://www.douban.com/group/topic/.*"))
        getTopics(topics)

        L = Url.split("=")
        newPageNumber = page + 25
        newUrl = L[0] + "=" + str(newPageNumber)
        getNextPage(newUrl, newPageNumber)
    except AttributeError:
        return



groupBag = set()
def findGroup(Url):
    global groupBag
    html = urlopen(Url)
    bs0bj = BeautifulSoup(html, "lxml")
    groupUrls = bs0bj.findAll("a", href=re.compile("https://www.douban.com/link2/.*"))
    for groupUrl in groupUrls:
        groupBag.add(groupUrl["href"])


search = input("Search: ")
homeUrl = "https://www.douban.com/search?cat=1019&q=%" + quote(search)
findGroup(homeUrl)


for groupUrl in groupBag:
    secondUrl = getFirstPage(groupUrl)
    if secondUrl == None:
        continue
    else:
        getNextPage(secondUrl, page=50)

# show the message
for title in sorted(topicBag, key=itemgetter(0), reverse=True):
    print(title)