import requests
from bs4 import BeautifulSoup
import time
import setting

url = "https://technews.tw/"
re = requests.get(url)
re.encoding = re.apparent_encoding
soup = BeautifulSoup(re.text,'html.parser')
previous_title = soup.find_all("h1",class_="entry-title")[1].a["title"]
tmp = []
tmp.append(previous_title)

while True:
    url = "https://technews.tw/"
    re = requests.get(url)
    re.encoding = re.apparent_encoding
    soup = BeautifulSoup(re.text,'html.parser')
    new_title = soup.find_all("h1",class_="entry-title")[0].a["title"]
    news_url = soup.find_all("h1",class_="entry-title")[0].a["href"]
    if previous_title != new_title and new_title not in tmp:
        headers = {
            "Authorization": "Bearer " + setting.token,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        params = {"message":"標題："+new_title+"\n"+"連結："+news_url}
        r = requests.post("https://notify-api.line.me/api/notify",
                        headers=headers, params=params)
        # print(r.status_code)  #200
        previous_title = new_title
        tmp.append(new_title)
    # print(title)
    # print(previous_title)
    if len(tmp)>5:
        del tmp[0]
    # print(tmp)

    time.sleep(10)
