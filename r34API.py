from xml.etree.ElementTree import fromstring
from config import config
import requests


class R34API:

    def __init__(self):
        self.__template = config['r34api']['template']
        self.__limit = config['r34api']['limit_per_request']

    def __constructRequest(self, tags=None, page: int = -1, enabledLimit=False):
        request = self.__template
        if tags is not None:
            request += '&tags='
            for tag in tags:
                request += (tag + '+')
        if enabledLimit:
            request += f'&limit={self.__limit}'
        if page != -1:
            request += f'&pid={page}'
        return request

    def __get(self, tags=None, page: int = -1, enabledLimit=False):
        return fromstring(
            requests.get(
                self.__constructRequest(tags, page, enabledLimit)
            ).text
        )

    def getPosts(self, amount: int, postTags: set = None, postFilter: set = None, page: int = -1, enabledLimit=False):
        if postTags is None:
            postTags = set()
        if postFilter is None:
            postFilter = set()

        any_in = lambda a, b: any(i in b for i in a)

        posts = []
        data = self.__get(postTags, page, enabledLimit)
        gotPostsValue = 0
        for child in data:
            if not any_in(child.attrib['tags'].split(), postFilter):
                posts.append(child.attrib['file_url'])
                gotPostsValue += 1
                if gotPostsValue == amount:
                    break

        return posts
