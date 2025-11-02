import urllib.request as req
import bs4
import csv

results=[]

def getTime(articleURL):
    request=req.Request(articleURL, headers={
        "cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    root = bs4.BeautifulSoup(data, "html.parser")
    times = root.find_all("span",class_="article-meta-value")
    if len(times)>=4:
        return times[3].string
    else:
        return ""

def getData(url):
    request=req.Request(url, headers={
        "cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")

    root=bs4.BeautifulSoup(data, "html.parser")
    titles=root.find_all("div", class_="title")
    likes=root.find_all("div", class_="nrec")

    for i in range(len(titles)):
        title=titles[i]
        like=likes[i]
        if title.a != None:
            link="https://www.ptt.cc"+title.a["href"]
            articleTitle=title.a.string
            likeCount=like.string
            publishTime=getTime(link)
            results.append([articleTitle,likeCount,publishTime])
    
    nextLink=root.find("a", string= "‹ 上頁")
    return nextLink["href"]

pageURL="https://www.ptt.cc/bbs/Steam/index.html"
count=0

while count<3:
    pageURL="https://www.ptt.cc"+getData(pageURL)
    count+=1

with open("articles.csv",mode="w",newline="",encoding="utf-8") as file:
    writer=csv.writer(file)
    writer.writerows(results)
        
