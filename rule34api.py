from xml.etree.ElementTree import fromstring
import requests


def makeRequestWithTags(tags):
    apiRequestTemplate = 'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&tags='
    for tag in tags:
        apiRequestTemplate += (tag + '+')
    return apiRequestTemplate


def getBasicRequest():
    return 'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index'


def getRecent(amount: int):
    response = fromstring(requests.get(getBasicRequest()).text)
    urls = []
    gotPostsValue = 0
    for child in response:
        urls.append(child.attrib['file_url'])
        gotPostsValue += 1
        if gotPostsValue == amount:
            break
    return urls


def getTagged(tags, amount: int):
    response = fromstring(requests.get(makeRequestWithTags(tags)).text)
    urls = []
    gotPostsValue = 0
    for child in response:
        urls.append(child.attrib['file_url'])
        gotPostsValue += 1
        if gotPostsValue == amount:
            break
    return urls


def hasTags(postTags, tagFilter):
    for tag in tagFilter:
        if tag in postTags:
            return True
    return False


def getTaggedWithFilter(tags, tagFilter, amount: int):
    response = fromstring(requests.get(makeRequestWithTags(tags)).text)
    urls = []
    gotPostsValue = 0
    for child in response:
        if not hasTags(child.attrib['tags'], tagFilter):
            urls.append(child.attrib['file_url'])
            gotPostsValue += 1
            if gotPostsValue == amount:
                break
    return urls


def makeRequestWithTagsCurrentPage(tags, page: int):
    baseRequest = makeRequestWithTags(tags)
    baseRequest += f'&pid={page}'
    return baseRequest

def getTaggedWithFilterCurrentPage(tags, tagFilter, amount: int, page: int):
    pass

