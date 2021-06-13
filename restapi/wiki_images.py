from bs4 import BeautifulSoup
import requests
import urllib.request
import regex as re
import shutil
import wget
url = 'https://en.wikipedia.org/wiki/Paris'
# get contents from url
content = requests.get(url).content
# get soup
soup = BeautifulSoup(content,'lxml') # choose lxml parser
# find the tag : <img ... >
image_tags = soup.findAll('img')
# print out image urls
i = 1
for image_tag in image_tags:
    link = image_tag.get('src')
    #image_link = link.split("/")[-1]
    #image_link = "https://en.wikipedia.org/wiki/Paris#/media/File:" + link
    #filename = link.split("/")[-1]
    filename = "Paris.jpg"
    if re.search('wikipedia/.*/thumb/', link) and not re.search('.svg', link):
        #print(image_tag.get('src'))
        if i == 1:
            i+=1
            image_link = "https:"+link
            #urllib.request.urlretrieve(image_link, filename)      #aku sakame da naprajme slika vo folder nekoj


            #r = requests.get(link[2:], stream=True)
            #i += 1
            #filename = wget.download(image_link)
            #print(image_link)
            #if r.status_code == 200:
            #    r.raw.decode_content = True
            #    with open(filename, 'wb') as f:
            #        shutil.copyfileobj(r.raw, f)
            #    print("image successfully downloaded")
            #else:
            #    print("didn't download")

            #print(image_link)