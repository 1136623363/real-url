# 获取快手直播的真实流媒体地址，默认输出最高画质
# https://live.kuaishou.com/u/KPL704668133
# 如获取失败，尝试修改 cookie 中的 did

import json
import re
import requests


class KuaiShou:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            # 'cookie': 'did=web_d563dca728d28b00336877723e0359ed',
        }
        with requests.Session() as s:
            url = 'https://live.kuaishou.com/u/{}'.format(self.rid)
            res = s.get(url, headers=headers)
            livestream = re.search(r'liveStream":(.*),"author', res.text)
            if livestream:
                livestream = json.loads(livestream.group(1))
                *_, hlsplayurls = livestream['playUrls']
                url = hlsplayurls['adaptationSet']['representation'][-1]['url']

                return url
            else:
                raise Exception('直播间不存在或未开播')


def get_real_url(rid):
    try:
        ks = KuaiShou(rid)
        return ks.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    # KPL704668133
    r = input('请输入快手直播房间ID：\n')
    print(get_real_url(r))
