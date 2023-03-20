# coding=UTF-8
import re
import uuid

from PIL import ImageFont

def generate_random_barcode():
    return ''.join(str(uuid.uuid1(clock_seq=18)).split('-'))[:18]

class Filter:
    @staticmethod
    def cutoff(code, length):
        if len(code) > length:
            code = code[:length]
        # print('filter.cutoff')
        return code
    @staticmethod
    def cutoffandComplete(code, length, complement=''):
        if len(code) > length:
            code = code[:length]
        if complement!='' and len(code) >length:
            code = code.ljust(18, complement)
        # print('filter.cutoff_and_complete')
        return code
    @staticmethod
    def equelLength(source, default):
        return source if len(source) == len(default) else default
    def onlyCN(source, default):
        return re.match(u"[\u4e00-\u9fa5]+",source).group() or default
    def onlyASCII(source, default):
        return re.match(u"[\x20-\x7e]+",source).group() or default
    @staticmethod
    def titleMap_DL2CSV(keyDL):
        mapdict = {
            'submitTime':'提交时间（自动）',
            'submitUser':'提交者（自动）',
            'nameCN':'你需要定制的姓名是？（必填）', 
            'nameEN':'你是否需要定制拼音或英文名，需要的话是？', 
            'birthDate': '你需要定制的日期是？（必填）', 
            'trCode': '年份',
            'barCode': '你需要定制的条形码内容是？（必填）', 
            'snCode':'条形码上方编号是？', 
            'orderID':'你的订单号是？（必填）',
            'otherCommits':'有什么别的备注？'
        }
        return mapdict[keyDL]


class DotDict(dict):
#   Example:
#   m = DotDict({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    def __init__(self, *args, **kwargs):
        super(DotDict, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(DotDict, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(DotDict, self).__delitem__(key)
        del self.__dict__[key]

class FontFamily:
    def __init__(self) -> None:
        self.EN = ImageFont.truetype(
            font="./resources/fonts/DINPro-Medium.otf")
        self.topEN = ImageFont.truetype(
            font="./resources/fonts/DINPro-Medium.otf", size=70)
        self.trCode = ImageFont.truetype(
            font="./resources/fonts/HarmonyOS_Sans_SC_Bold.ttf", size=120)
        self.CN = ImageFont.truetype(
            font="./resources/fonts/HarmonyOS_Sans_SC_Regular.ttf", size=220)
        self.snCode = ImageFont.truetype(
            font="./resources/fonts/HarmonyOS_Sans_SC_Medium.ttf", size=80)
        self.CN_l = ImageFont.truetype(
            font="./resources/fonts/HarmonyOS_Sans_SC_Regular.ttf", size=200)
        pass
    @classmethod
    def CNwithLength(self, isLongName=0):
        size = 200 if isLongName>0 else 220
        return ImageFont.truetype(
            font="./resources/fonts/HarmonyOS_Sans_SC_Regular.ttf", size=size)

pxlFont = FontFamily()