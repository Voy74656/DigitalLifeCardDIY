# coding=UTF-8
import getopt
import re
import sys
import uuid

from PIL import Image, ImageDraw, ImageFont


import barcode
from barcode.writer import ImageWriter as bcWriter

from xpinyin import Pinyin
DEAFULT_PINYIN = Pinyin()

from collections import namedtuple

BARCODETEMPDIR = './tmp/'

BARCODE_UUID_ENABLE = '__UUID__'


rawDigitalLifeUV = namedtuple('dataDigitalLifeUV', [
                               'nameCN', 'nameEN', 'birthDate', 'trCode', 'barCode', 'snCode', 'basePNG'])
rawDigitalLifeUV.__new__.__defaults__ = ( '图丫丫',
                                           'TUYAYA',
                                           '19000101',
                                           '2023',
                                           ''.join(str(uuid.uuid1(clock_seq=18)).split('-'))[:18],
                                           'PN-R-DSM01 A513C',
                                           '水贴底图 4K B.png')

# DEFAULT_DL = rawDigitalLifeUV('图丫丫', 'TUYAYA', '19000101', '2023', ''.join(str(uuid.uuid1(clock_seq=18)).split('-'))[:18], 'PN-R-DSM01 A513C', '水贴底图 4K B.png')
DEFAULT_DL = rawDigitalLifeUV()

def get_pinyin(nameCN, pinyin=DEAFULT_PINYIN):
    return pinyin.get_pinyin(nameCN, splitter='', convert='upper') or DEFAULT_DL.nameEN


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
            'nameCN':'中文姓名', 
            'nameEN':'拼音或英文名', 
            'birthDate': '生日', 
            'trCode': '右上年份',
            'barCode': '条形码数据', 
            'snCode':'SN码', 
            'orderID':'淘宝订单号'
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
            font="./necessary fonts/DINPro-Medium.otf")
        self.topEN = ImageFont.truetype(
            font="./necessary fonts/DINPro-Medium.otf", size=70)
        self.trCode = ImageFont.truetype(
            font="./necessary fonts/HarmonyOS_Sans_SC_Bold.ttf", size=120)
        self.CN = ImageFont.truetype(
            font="./necessary fonts/HarmonyOS_Sans_SC_Regular.ttf", size=220)
        self.snCode = ImageFont.truetype(
            font="./necessary fonts/HarmonyOS_Sans_SC_Medium.ttf", size=80)
        self.CN_l = ImageFont.truetype(
            font="./necessary fonts/HarmonyOS_Sans_SC_Regular.ttf", size=200)
        pass
    @classmethod
    def CNwithLength(self, isLongName=0):
        size = 200 if isLongName>0 else 220
        return ImageFont.truetype(
            font="./necessary fonts/HarmonyOS_Sans_SC_Regular.ttf", size=size)

pxlFont = FontFamily()

class singleDigitalLifeUV:
    def __init__(self, data, exportImgTypes:list=['tif','png']) -> None:
        if isinstance(data, str):
            data = self._fromCfg(file=data)
        if isinstance(data,dict):
            data = DotDict(data)
        if not isinstance(data, (rawDigitalLifeUV, DotDict)):
            return
        self.nameCN = Filter.cutoff(Filter.onlyCN(data.nameCN, DEFAULT_DL.nameCN), 4)
        self.nameEN = Filter.onlyASCII(data.nameEN, get_pinyin(self.nameCN)) 
        self.birthDate = Filter.equelLength(Filter.onlyASCII(data.birthDate, DEFAULT_DL.birthDate), DEFAULT_DL.birthDate)
        self.trCode = Filter.equelLength(Filter.onlyASCII(data.trCode, DEFAULT_DL.trCode), DEFAULT_DL.trCode)
        self.barCode = Filter.cutoffandComplete(Filter.onlyASCII(data.barCode, DEFAULT_DL.barCode), 18, '-')
        self.snCode = Filter.cutoff(Filter.onlyASCII(data.snCode, DEFAULT_DL.snCode), 20)
        self.basePNG = data.basePNG

        # private parameters
        self._exportImgTypes = exportImgTypes
        self._barcodeTmpDir = BARCODETEMPDIR
        # self._outputPath=outputPath
        pass

    @classmethod
    def from_cli(self):
        nameCN = input(f'输入名字，最多四个字，仅截取中文，默认为{DEFAULT_DL.nameCN}：') or DEFAULT_DL.nameCN

        nameEN = get_pinyin(Filter.cutoff(nameCN, 4))
        if input(f'\n名字拼音为：{nameEN}\n是否修改输入拼音/英文名？\n输入y进入手动输入，不输入或输入其他跳过\n') == 'y':
            nameEN = input("\n输入名字拼音或英文名。支持ASCII字符：\n").upper()
        print(f'英文名已经设置为：{nameEN}')

        birthDate = input(f'\n输入生日，示例：{DEFAULT_DL.birthDate}：\n') or DEFAULT_DL.birthDate

        barCode = input(
        "\n输入条形码内容，\n 格式为18个非中文字符\n输入__UUID__可以自动生成18位随机字符\n也可以输出自定义输入，少于18位会自动使用 - 填补\n").ljust(18, '-')  # 条形码内容
        if barCode.upper() == BARCODE_UUID_ENABLE.ljust(18, '-'):
            barCode = ''.join(str(uuid.uuid1(clock_seq=18)).split('-'))[:18]
        print(f'条形码已经设置为：{barCode}')

        trCode = input("\n顶部年份，固定四位\n也可自定义为其他四位短语，仅支持非中文字符\n，示例：1900，CM02等：\n")  # 顶部年份

        snCode = input("\n输入自定义sn码\n不输入即为默认(PN-R-DSM01 A513C)\n") or DEFAULT_DL.snCode  # 生日

        return singleDigitalLifeUV(rawDigitalLifeUV(nameCN, nameEN, birthDate, trCode, barCode, snCode))
    


    def export(self, suffix:str = '', outputPath='./output/', filenameOveride=None):
        assert suffix in ['tif','png','json',''], "illegal output file type !"
        if suffix == 'json':
            return self.__dict__
        _filename = filenameOveride if filenameOveride else self.nameCN
        _img = self._radar_img()
        if suffix == '':
            for sf in self._exportImgTypes:
                self._imgsavewarpper(_img, f'{outputPath}{_filename}.{sf}')
        else:
            self._imgsavewarpper(_img, f'{outputPath}{_filename}.{sf}')        

    def _radar_img(self):
        img = Image.open(fp=self.basePNG)
        draw = ImageDraw.Draw(img)
        # 添加姓名
        _islongname = len(self.nameCN) > 3
        _font = pxlFont.CN_l if _islongname else pxlFont.CN
        draw.text(xy=(580, 1000 + _islongname*10), text=self.nameCN, fill=(255, 255, 255), font=_font)
        # # 添加姓名拼音加日期
        _top_left_str = " ".join(re.findall(".{1}", self.nameEN + '-A' + self.birthDate))
        draw.text(xy=(2440 - len(_top_left_str) * 38, 142),
              text=_top_left_str, fill=(255, 255, 255), font=pxlFont.topEN)
        # 添加顶部后边的年份
        draw.text(xy=(2515, 120), text=self.trCode, fill=(255, 255, 255), font=pxlFont.trCode)
        # 添加条码上的文字
        draw.text(xy=(2705 - len(self.snCode) * 40, 1010), text=self.snCode,
              fill=(255, 255, 255), font=pxlFont.snCode)
        # 添加条码
        b_code_img = self._gen_barcode(self.barCode, self._barcodeTmpDir)
        img.paste(b_code_img, (1380, 1110))
        return img

    def _imgsavewarpper(self, img:Image, filename:str):
        try:
            img.save(f'{filename}')
            print(f'\n{filename} 生成成功！')
        except:
            print(f'\n{filename} 生成失败！\n')

    @staticmethod
    def _fromCfg(file: str) -> rawDigitalLifeUV:
        return

    @staticmethod
    def _gen_barcode(text, output='', barcodeTmpDir=BARCODETEMPDIR):
        b = barcode.get("code128", text, writer=bcWriter())
        b.save(f'{barcodeTmpDir}barcode')
        with open(f'{barcodeTmpDir}barcode.png', "rb") as f:
            barcodeimg = Image.open(fp=f)
            barcodeimg = barcodeimg.crop((20, 20, 600, 50))
            # barcodeimg.save("./output/barcode_crop.png")
            bin = barcodeimg.convert("1")
            bin = bin.resize((1500, 105))
            barcodeimg = barcodeimg.resize((1500, 105))
            barcodeimg = barcodeimg.convert("RGBA")
            W, H = barcodeimg.size
            for x in range(W):
                for y in range(H):
                    if bin.getpixel((x, y)) == 255:
                        barcodeimg.putpixel((x, y), (255, 255, 255, 0))
                    else:
                        barcodeimg.putpixel((x, y), (255, 255, 255, 255))
            # barcodeimg.save("./output/barcode_bin.png")
            return barcodeimg


class DigitalLifeUVs:
    def __init__(self, data) -> None:
        if isinstance(data,str):
            self.data = self.readfromCSV(data)
            return
        assert isinstance(data,list), 'date Type error'
        self.data = {idx+1:dl for idx, dl in enumerate(data) if isinstance(dl, singleDigitalLifeUV)}
        pass
    def export(self, suffix:str = '', outputPath='./output/'):
        for id, dl in self.data.items():
            dl.export(suffix=suffix, outputPath=outputPath, filenameOveride=id+'_'+dl.nameCN)
    @staticmethod
    def readfromCSV(filename):
        import csv
        data = {}
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                ordered_id = row[Filter.titleMap_DL2CSV('orderID')]
                # data = {Filter.titleMap_DL2CSV(i):row[Filter.titleMap_DL2CSV(i)] for i in }
                # d = DEFAULT_DL._asdict()
                d = {k:row[Filter.titleMap_DL2CSV(k)] for k,_ in DEFAULT_DL._asdict().items() if k!='basePNG'}
                d['basePNG'] = DEFAULT_DL.basePNG
                data[ordered_id] = singleDigitalLifeUV(d)
        return data
        



if __name__ =="__main__":
    opts, args = getopt.getopt(sys.argv[1:], '-h-c-g:-o:-v', ['help','cil','group', 'output', 'version'])
    def help():
        print(f'USAGE:\n\n    python {__file__} [opt]\n\nopts:\n'+
              '        -c / --cil:                   (DEFAULT) Generate DigitalLife Card UV in console.\n'+
              '        -g / --group [csv file]:      Auto generate DigitalLife Card UVs for group.\n'+
              '        -o / --output [output path]:  Set output dir, can work with -c and -g command\n'+
              '                                      Dafault: ./output/\n'
              '        -v / --version:               Display script version & developer\'s information\n'+
              '        -h / --help:                  Display this help file')
        sys.exit()
    def version():
        print(f'Version 2.0\nBy @Voy74654\nrefer: \n    [github] https://github.com/Voy74656/DigitalLifeCardDIY\n    [gitee]  https://gitee.com/Voy74656/DigitalLifeCardDIY')
        sys.exit()
    
    OUTPUT_PATH='./output/'
    data = None

    for opt_name, opt_value in opts:
        if opt_name in ('-h', '--help'):
            help()
        if opt_name in ('-v', '--version'):
            version()
        if opt_name in ('-g', '--group'):
            data = DigitalLifeUVs(opt_value)
        if opt_name in ('-o', '--output'):
            OUTPUT_PATH = opt_value
        if opt_name in ('-c', '--cil'):
            data = singleDigitalLifeUV.from_cli()
    if not data:
        data = singleDigitalLifeUV.from_cli()
    data.export(outputPath=OUTPUT_PATH)
    sys.exit()

    ####### __MAIN__ END #######



    ####### advance #######

    # expose api 
    # dl1 = rawDigitalLifeUV('爱莉希雅','EGO-ALYSIA','20211111','CM02','Qjxie1234567890efx','Miss Pink Elf ~')
    # dls = DigitalLifeUVs([dl1, dl1, dl1])