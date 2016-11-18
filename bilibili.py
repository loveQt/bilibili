# -*-coding:utf8-*-
import re
import utils

_bilibili_URL = 'http://www.bilibili.com/'
_bilibili_space_URL = 'http://space.bilibili.com/'
_bilibili_av_info_prefix = 'http://interface.bilibili.com/count?key=5febfb9006283a2e07e6f711&aid='
_bilibili_user_info_prefix = ''

_av_api_pattern = re.compile('\d{1,10}')
_av_up_pattern = re.compile('<a class="up-name" href="http://space.bilibili.com/(.*)#!/" target="_blank">UP主: (.*)</a>')


# _m_header = {
#     'User-Agent':'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E)'
# }

# def _parser_user_from_uid(uid, name=None):
#     user_obj = User(uid, name=name)
#     return user_obj


class AV:
    def __init__(self, aid, url=None, title=None, up=None, replay=None, stow=None, coin=None, dm_count=None):
        self._aid = aid
        self._url = url
        self._title = title
        self._up = up
        self._replay = replay
        self._stow = stow
        self._coin = coin
        self._dm_count = dm_count
        self._api = _av_api_pattern.findall(utils.get_html(_bilibili_av_info_prefix + str(self._aid)))
        self._html = utils.get_html('http://www.bilibili.com/mobile/video/av' + str(self._aid) + '.html')

    @property
    def url(self):
        return _bilibili_URL + 'video/av' + str(self._aid)

    @property
    def title(self):
        return re.search(r'<title>(.*)_.*bilibili_', self._html).group(1)

    @property
    def up(self):
        up_info = _av_up_pattern.search(self._html)
        up_id = up_info.group(1)
        up_name = up_info.group(2)
        return User(up_id, name=up_name)

    # @property
    def get_videos(self):
        videos = []
        cids = []
        urls = []
        titles = []
        av_url = 'http://www.bilibili.com/video/av' + str(self._aid) + '/'
        pattern1 = re.compile(r'/video/av.*/(index_.*).html')
        pattern2 = re.compile(r'cid=(\d{5,10})&aid=(\d{5,10})&pre')
        pattern3 = re.compile(r'\>(.+)</option>')
        av_content = utils.get_html(av_url)
        indexes = pattern1.findall(av_content)
        titles = pattern3.findall(av_content)

        if not len(indexes):  # not == []
            cids.append(pattern2.search(av_content).group(1))
            url = self.url
            title = self.title
            urls.append(url)
            titles.append(title)
        else:
            for index in indexes:
                url = 'http://www.bilibili.com/video/av' + str(self._aid) + '/' + index + '.html'
                urls.append(url)
        for url in urls:
            # cid_url = 'http://www.bilibili.com/video/av' + str(self._aid) + '/' + index + '.html'
            cid_content = utils.get_html(url)
            cid = pattern2.search(cid_content).group(1)
            cids.append(cid)
        videos = zip(cids, urls, titles)
        return videos
        # return utils.get_cids(self._aid)

    # def urls(self):
    #     return

    @property
    def replay(self):
        return self._api[1]

    @property
    def stow(self):
        return self._api[2]

    @property
    def coin(self):
        return self._api[3]

    @property
    def dm_count(self):
        return self._api[5]

    @property
    def comment(self):
        return Comment()

    @property
    def videos(self):
        # for cid, url in zip(self.cids, self.urls):
        for video in self.get_videos():
            yield Video(cid=video[0], url=video[1], title=video[2], aid=self._aid)


class Video:
    def __init__(self, cid, url=None, title=None, aid=None):
        self._cid = cid
        self._url = url
        self._title = title

    @property
    def url(self):
        # http: // www.bilibili.com / video / av637684 / index_2.html
        return _bilibili_URL + 'video/av' + str(self._cid)

    @property
    def danmu(self):
        return Danmu(self._cid)

    def download_danmu(self):
        pass


class User:
    def __init__(self, uid, url=None, name=None, sex=None, reg_date=None):
        self._uid = uid
        self._url = url
        self._name = name
        self._sex = sex
        self._reg_date = reg_date

    @property
    def url(self):
        return _bilibili_space_URL + str(self._uid)

    @property
    def name(self):
        return

    @property
    def sex(self):
        return

    @property
    def reg_date(self):
        return

    @property
    def birthday(self):
        return

    @property
    def place(self):
        return

    @property
    def attention(self):
        return

    @property
    def fans(self):
        return

    @property
    def level(self):
        return

    @property
    def exp(self):
        return

    @property
    def tag(self):
        return

    @property
    def av_tag(self):
        return


class Comment:
    def __init__(self):
        pass


class Danmu:
    def __init__(self, cid):
        pass


av = AV(7148183)
up_ = av.up
# print av
print av.url
# print av.videos
avc = av.videos
print avc
for v in avc:
    print v._cid
    print v._url
    print v._title
# print av.cids
print av.replay, av.stow, av.coin, av.dm_count, av.title, up_.url
