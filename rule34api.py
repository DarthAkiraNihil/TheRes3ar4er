from xml.etree.ElementTree import fromstring
import requests

LIMIT_PER_REQUEST = 30


def makeRequestWithTags(tags, enableLimit=False):
    apiRequsestTemplate = str()
    if enableLimit:
        apiRequestTemplate = f'https://api.rule34.xxx/index.php?page=dapi&s=post' + \
                             '&q=index&limit={LIMIT_PER_REQUEST}&tags='
    else:
        apiRequestTemplate = 'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&tags='
    for tag in tags:
        apiRequestTemplate += (tag + '+')
    return apiRequestTemplate


def getBasicRequest(enabledLimit=False):
    if enabledLimit:
        return 'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index' + f'&limit{LIMIT_PER_REQUEST}'
    else:
        return 'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index'


def getRecent(amount: int, enabledLimit=False):
    response = fromstring(requests.get(getBasicRequest(enabledLimit)).text)
    urls = []
    gotPostsValue = 0
    for child in response:
        urls.append(child.attrib['file_url'])
        gotPostsValue += 1
        if gotPostsValue == amount:
            break
    return urls


def getTagged(tags, amount: int, enabledLimit=False):
    response = fromstring(requests.get(makeRequestWithTags(tags, enabledLimit)).text)
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


def getTaggedWithFilter(tags, tagFilter, amount: int, enabledLimit=False):
    response = fromstring(requests.get(makeRequestWithTags(tags, enabledLimit)).text)
    urls = []
    gotPostsValue = 0
    for child in response:
        if not hasTags(child.attrib['tags'], tagFilter):
            urls.append(child.attrib['file_url'])
            gotPostsValue += 1
            if gotPostsValue == amount:
                break
    return urls


def makeRequestWithTagsCurrentPage(tags, page: int, enabledLimit=False):
    baseRequest = makeRequestWithTags(tags, enabledLimit)
    baseRequest += f'&pid={page}'
    return baseRequest


def getTaggedCurrentPage(tags, amount: int, page: int, enabledLimit=False):
    response = fromstring(requests.get(makeRequestWithTagsCurrentPage(tags, page, enabledLimit)).text)
    urls = []
    gotPostsValue = 0
    for child in response:
        urls.append(child.attrib['file_url'])
        gotPostsValue += 1
        if gotPostsValue == amount:
            break
    return urls


def getTaggedWithFilterCurrentPage(tags, tagFilter, amount: int, page: int, enabledLimit=False):
    response = fromstring(requests.get(makeRequestWithTagsCurrentPage(tags, page, enabledLimit)).text)
    urls = []
    gotPostsValue = 0
    for child in response:
        if not hasTags(child.attrib['tags'], tagFilter):
            urls.append(child.attrib['file_url'])
            gotPostsValue += 1
            if gotPostsValue == amount:
                break
    return urls
