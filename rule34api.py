from xml.etree.ElementTree import fromstring
import requests


def makeRequestWithTags(tags):
    apiRequestTemplate = 'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&tags='
    for tag in tags:
        apiRequestTemplate += (tag + '+')
    return apiRequestTemplate


def getBasicRequest():
    return 'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index'


def getRecent(amount):
    response = fromstring(requests.get(getBasicRequest()).text)
    urls = []
    gotPostsValue = 0
    for child in response:
        urls.append(child.attrib['file_url'])
        gotPostsValue += 1
        if gotPostsValue == amount:
            break
    return urls


def getTagged(tags, amount):
    response = fromstring(requests.get(makeRequestWithTags(tags)).text)
    urls = []
    gotPostsValue = 0
    for child in response:
        urls.append(child.attrib['file_url'])
        gotPostsValue += 1
        if gotPostsValue == amount:
            break
    return urls

