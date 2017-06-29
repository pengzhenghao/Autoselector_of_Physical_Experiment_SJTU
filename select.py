# -*- coding:utf-8 -*-
import re
import urllib.parse
import urllib.request
from http import cookiejar

LOGINID = 000000000000
PASS = 00000000
WEEK = [10, 16]
EXPNAME = [u'真空镀膜', u'RLC电路特性的研究', u'用非线性电路研究混沌现象', u'非平衡电桥的应用', u'硅光电池特性的研究', u'磁性材料基本特性的研究']
TIME = '2B'


class Selection(object):
    # Constructor

    header = {'Accept-Encoding': 'gzip, deflate',
              'Cache-Control': 'max-age=0',
              'Upgrade-Insecure-Requests': '1',
              'Host': '202.120.52.55',
              'Content-Type': 'application/x-www-form-urlencoded',
              'Connection': 'keep-alive',
              'Accept-Language': 'zh-CN,zh;q=0.8',
              'Referer': 'http://202.120.52.55/pe/',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Origin': 'http://202.120.52.55',
              }

    def login(self):

        ck = cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(ck))

        request = urllib.request.Request('http://202.120.52.55/pe/default.aspx')
        response = self.opener.open(request)
        pattern = re.compile(r'name="__VIEWSTATE" value="(.*)" />')
        VIEWSTATE = re.search(pattern, response.read().decode('gb2312'))

        data = {'login1:btnLogin.x': '38',
                'login1:btnLogin.y': '19',
                'login1:StuPassword': PASS,
                'login1:StuLoginID': LOGINID,
                'login1:UserRole': 'Student'}

        data['__VIEWSTATE'] = str(VIEWSTATE.group(1))
        postData = urllib.parse.urlencode(data)
        request = urllib.request.Request('http://202.120.52.55/pe/default.aspx', postData.encode(), self.header)
        result = self.opener.open(request)

        if re.search('515021910506', result.read().decode('gb2312')):
            print("Login Succeed!")
        else:
            print("Login Failed!")

    def update(self, data_encoded):
        if data_encoded != None:
            postData = urllib.parse.urlencode(data_encoded)
            request = urllib.request.Request('http://202.120.52.55/pe/student/addexpe.aspx', postData.encode(),
                                             self.header)
        else:
            request = urllib.request.Request('http://202.120.52.55/pe/student/addexpe.aspx', headers=self.header)
        return self.opener.open(request)

    def addExp(self, exp):
        # 1,enter the addexpe page.
        req = urllib.request.Request('http://202.120.52.55/pe/student/addexpe.aspx', headers=self.header)
        response = self.opener.open(req)
        pattern = re.compile(r'name="__VIEWSTATE" value="(.*?)" />')
        VIEWSTATE = re.search(pattern, response.read().decode('gb2312'))

        # 2,choose week.
        data = {'__EVENTTARGET': 'ExpeWeekList',
                '__EVENTARGUMENT': '',
                '__VIEWSTATE': VIEWSTATE.group(1),
                'ExpeWeekList': exp['week'],
                'ExpeClassList': 'D1',
                't1': ''}
        req = urllib.request.Request('http://202.120.52.55/pe/student/addexpe.aspx',
                                     urllib.parse.urlencode(data).encode(), self.header)
        response = self.opener.open(req)
        VIEWSTATE = re.search(pattern, response.read().decode('gb2312'))

        # 3,choose day.
        data = {'__EVENTTARGET': 'ExpeTimeList',
                '__EVENTARGUMENT': '',
                '__VIEWSTATE': str(VIEWSTATE.group(1)),
                'ExpeWeekList': exp['week'],
                'ExpeTimeList': exp['time'],
                'ExpeClassList': 'D1',
                't1': ''}
        req = urllib.request.Request('http://202.120.52.55/pe/student/addexpe.aspx',
                                     urllib.parse.urlencode(data).encode(), self.header)
        response = self.opener.open(req)
        tempread = response.read().decode('gb2312')
        VIEWSTATE = re.search(pattern, tempread)

        a = '<option value="(.*?)">' + exp['name']
        pattern_lesson = re.compile(a)

        try:
            nameCode = re.search(pattern_lesson, tempread).group(1)
            print(exp['name'], ' nameCode:', nameCode)
        except AttributeError as a:
            print("Can't find", exp['name'])
            return False

        # 4,choose exp and SIGN IN.
        data = {'__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                '__VIEWSTATE': str(VIEWSTATE.group(1)),
                'ExpeWeekList': exp['week'],
                'ExpeTimeList': exp['time'],
                'ExpeClassList': 'D1',
                'ExpeNameList': nameCode,
                'btnAdd.x': '21',
                'btnAdd.y': '14',
                't1': 'yeduo'}

        postData = urllib.parse.urlencode(data)
        request = urllib.request.Request('http://202.120.52.55/pe/student/addexpe.aspx', postData.encode(), self.header)
        response = self.opener.open(request)
        pattern = re.compile(r'<span id="Tip"><font color="Red">(.*?)</font></span></td>')
        searchresult = pattern.search(response.read().decode('gb2312')).group(1)
        print("__________")
        print(searchresult)
        if searchresult == u'该实验选修成功':
            return True
        else:
            return False

    def main(self):
        print("Process Begin")
        name = EXPNAME
        flag = False
        for i in range(WEEK[0], WEEK[1]):
            for n in name:
                tmp = {'week': str(i), 'time': TIME, 'name': n}
                if self.addExp(tmp):
                    print('选择', tmp['name'], '成功')
                    name.remove(n)
                    flag = True
                else:
                    print('选择', tmp['name'], '失败')
                print("__________")
                if flag:
                    flag = False
                    break


if __name__ == '__main__':
    print("""　　　　　　　　　　　　　　　　　　▁▁▁　　　　　　　　　　　　　　　　　　　　　　　
    　　　　　　　　　丶丶　　丶丶丶丶丶　　　丶十日瓦車鬼鬼車毋己十丶　　丶丶丶　　　　　　　　　　丶　
    　　　　　　　　丶丶丶　丶丶丶丶　丶十日毋馬龠齱龍龍龍龍齱齱齱龍馬日丶　　丶丶　　　　　　　　　　　
    　　　　　　　　丶丶丶丶丶丶丶　亅日毋車車馬龍龠龠龠龠龍龍龍龍龍龍龍龠瓦丶　丶　　　　　　　　　　　
    　　　　　　　　丶丶丶丶丶丶　十瓦日日車鬼鬼馬龠鬼馬龠龍龍龍馬龠龠馬龍龍毋丶　　　　　　　　　　　　
    　　　　　　　丶　　　丶　　乙鬼馬龠龠龠龠龠龠龠馬瓦毋馬龠龠鬼車鬼鬼龠龠龠馬己　　　　　　　　　　　
    　　　　　　　　　　　　　己龠龍龍龍龍龍馬鬼鬼車毋十丶十乙己乙亅乙日車鬼馬龍龍毋　　　　　　　　　　
    　　　　　　　　　　　　己龠龍馬馬龠馬瓦己十丶亅丶　　　　　　　丶丶十己龠龍龠齱毋　　　　　　　　　
    　　　　　　　　　　　丶鬼龠龠馬馬車乙丶　　　　　　　　　　　　丶丶丶丶日馬龠龠龍乙　　　　　　　　
    　　　　　　　　　　　十龠龠龠龠車己丶　　　　　　　　　　　　　丶丶丶亅亅日龍龠龍車　　　　　　　　
    　　　　　　　　　　　日龍龠龠鬼毋十　　　　　　　　　　　　　　丶丶丶亅亅十車龠龍龍亅　　　　　　　
    　　　　　　　　　　　毋龍龠龠馬毋亅　　　　　　　　　　　　　　丶丶亅丶亅亅瓦龠龠龍日　　　　　　　
    　　　　　　　　　　　鬼龍龠馬鬼日亅　　　　　　　　　　　　　　丶丶丶丶丶亅乙車龠龍鬼　　　　　　　
    　　　　　　　　　　丶馬馬馬馬毋己丶丶　　　　　　　　　　　　　　丶丶丶亅亅乙毋龠龍馬丶　　　　　　
    　　　　　　　　　　亅馬鬼馬龠瓦亅丶丶　　　　　　　　　　　　　　丶丶丶亅亅乙瓦馬龍馬丶　　　　　　
    　　　　　　　　　　乙龠馬龠馬瓦亅丶丶　　　　　　　　　　　　　　　丶丶亅十乙瓦馬龍車　　　　　　　
    　　　　　　　　　　己龍龠龠鬼乙丶丶丶　　　　　　　　　　　　　　　丶亅丶亅十日馬龍毋　　　　　　　
    　　　　　　　　　　十龠龍馬馬己　　　乙車日乙己己瓦瓦日十　　　亅日瓦日日瓦車車馬龍乙　　　　　　　
    　　　　　　　　　　　十車龠龍龠鬼己日馬己丶丶丶丶十毋龠龠亅　乙龠鬼日己日車鬼馬龍鬼　　　　　　　　
    　　　　　　　　　　　　乙車車車鬼龠齱毋亅丶亅乙己日十亅毋龠馬龍瓦亅亅瓦日日車車龍馬丶　　　　　　　
    　　　　　　　　　　　　　亅　　　十馬乙　丶乙十乙車日丶十龠龍龠十十亅車車毋瓦鬼鬼龠亅　　　　　　　
    　　　　　　　　　　　　　丶　　　　己亅　　　　　丶十丶己日十鬼亅丶　丶亅十乙日己車　　　　　　　　
    　　　　　　　　　　　　　　　　　　十十　　　丶丶亅丶丶車十丶鬼亅丶亅亅亅丶亅十己十　　　　　　　　
    　　　　　　　　　　　　　　　　　　丶乙　　　丶丶丶　日車　丶毋日　丶丶丶丶丶亅瓦丶　　　　　　　　
    　　　　　　　　　　　　　　　　　　　乙己亅丶　　丶己車亅　　乙馬十　丶　　　己己　　　　　　　　　
    　　　　　　　　　　　　　　　　　　　　乙日日己乙日日丶　　　丶己車日己乙己日毋亅　　　　　　　　　
    　　　　　　　　　　　丶　　　　　　　　　　　亅亅亅丶亅亅　　十十亅十乙乙乙亅乙丶　　　　　　　　　
    亅亅十十十十十乙十十瓦龠毋　　　　　丶　丶丶丶丶　丶亅十己乙己日己十丶丶丶丶十瓦丶　　　　　　　　　
    鬼車鬼鬼馬馬馬馬馬馬龠馬龠車十　丶　　丶丶亅亅丶丶丶　　　十乙亅亅亅亅亅十十日瓦丶　　　　　　　　　
    車毋車車鬼鬼馬馬馬馬馬車馬齱瓦　丶丶　丶丶亅丶丶丶　　　　　　丶丶亅十十十十乙毋鬼十　　　　　　　　
    車毋車車車鬼馬馬馬馬馬車馬龍毋　丶丶丶丶丶丶丶亅亅丶亅亅丶亅十十十乙日亅亅亅乙鬼龠龠己　　　　　　　
    車毋毋車鬼鬼馬馬馬馬鬼鬼馬龠毋丶丶丶丶丶丶丶丶亅車鬼日乙亅十十己車鬼乙丶亅亅日龠馬龠龠瓦亅　　　　　
    車毋毋車鬼鬼馬馬馬馬鬼鬼馬鬼毋十　丶丶丶丶丶丶　十毋車瓦日日日車鬼十丶亅亅乙鬼龠馬馬馬龠馬車乙　　　
    毋毋車車鬼鬼馬馬馬馬鬼鬼鬼毋車日　丶丶丶丶丶丶丶　　丶十乙己瓦日乙亅亅亅十毋龍龠龠馬馬馬馬龠龠瓦亅　
    毋毋毋車鬼馬馬馬馬馬馬鬼車毋車毋丶丶丶丶丶丶丶丶　　　　丶亅十乙十亅亅十日龠龠龠龠馬馬馬馬馬馬龠龠瓦
    毋毋毋車鬼馬馬馬馬馬龠鬼車毋毋車己　丶丶丶丶　　　　　丶丶亅亅亅十亅亅日馬龍龠龠馬馬馬馬馬馬馬馬龠龠
    毋毋毋車車鬼馬龠馬馬龠馬車車車車鬼十　丶丶丶　　　　　　丶丶丶亅亅亅日馬龍龠龠龠龠馬馬馬馬馬馬馬馬馬
    毋毋毋毋車鬼鬼馬馬馬馬龠鬼車車車鬼鬼丶　丶丶丶丶　　　　　　丶丶亅乙龠龍龠龠龠龠龠龠馬馬馬馬馬馬馬馬
    毋毋毋毋車車鬼鬼馬馬馬馬鬼車車車車馬毋　　丶亅丶　丶丶丶丶丶丶亅十鬼龍龠龠龠龠龠龠龠龠龠馬馬馬馬馬馬
    毋毋車車車車車鬼鬼馬馬馬鬼車車車鬼鬼馬毋　　亅十乙十亅亅十十乙日馬龍龠龠龠龠龠龠龠龠龠龠龠馬馬馬馬鬼
    毋毋車車車車車鬼鬼鬼馬馬馬鬼車車鬼鬼鬼龠車亅　亅己車鬼鬼鬼馬龠龍龍龠龠龠龠龠龠龠龠龠龠龠龠馬馬馬馬鬼
    毋瓦毋車車鬼鬼鬼鬼鬼鬼馬馬鬼鬼鬼鬼鬼鬼鬼龠龠日己瓦鬼龍龍龍龍龍龠龠龠龠龠龠龠龠龠龠龠龠馬馬馬馬馬馬鬼
    毋瓦毋車車鬼鬼鬼鬼鬼鬼鬼馬鬼鬼鬼鬼鬼鬼鬼龠龠鬼龠龍龍龠龠龠龠龠龠龠龠龠龠龠龠龠龠龠龠馬馬馬馬馬馬馬鬼
    毋毋車車車鬼鬼鬼鬼鬼鬼鬼鬼馬鬼鬼鬼鬼鬼馬龍毋毋龍龠龠龠龠龠龠龠龠龠龠龠龠龠龠龠龠龠龠龠龠馬馬馬馬馬鬼
    鬼車鬼鬼馬馬鬼鬼鬼馬馬馬馬馬馬鬼鬼鬼馬龠龠瓦毋龍龠龠龠龠龠龠龠龠龠龠龠龠龠龠龠龠龠龠龠龠龠馬馬馬馬馬

                    基于Python的上海交通大学物理实验自动化选择程序(匿名开发者)
    Automatic Selection Program for Physical Experiment Based On Python3(Anonymous Developer)

    """)
    a = Selection()
    a.login()
    a.main()
    print("Process End")
