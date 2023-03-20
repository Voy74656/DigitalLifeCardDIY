
# coding=UTF-8
import re
import uuid

import base64

from PIL import Image, ImageDraw

import barcode
from barcode.writer import ImageWriter as bcWriter
from collections import namedtuple

from lib.utils import DotDict, Filter

from lib.config import BARCODE_TEMP_DIR, BARCODE_UUID_ENABLE_KEY, BASE_IMAGE, DEAFULT_PINYIN, DEFAULT_BARCODE, DEFAULT_BIRTH_DATE, DEFAULT_FONTFAMILY, DEFAULT_NAME_CN, DEFAULT_NAME_EN, DEFAULT_SN_CODE, DEFAULT_TOP_RIGHT_CODE


def _get_pinyin(nameCN, pinyin=DEAFULT_PINYIN):
    return pinyin.get_pinyin(nameCN, splitter='', convert='upper') or DEFAULT_NAME_EN


rawDigitalLifeUV = namedtuple('dataDigitalLifeUV', [
    'nameCN', 'nameEN', 'birthDate', 'trCode', 'barCode', 'snCode', 'basePNG'])
rawDigitalLifeUV.__new__.__defaults__ = (DEFAULT_NAME_CN,
                                         DEFAULT_NAME_EN,
                                         DEFAULT_BIRTH_DATE,
                                         DEFAULT_TOP_RIGHT_CODE,
                                         DEFAULT_BARCODE,
                                         DEFAULT_SN_CODE,
                                         BASE_IMAGE)

default_dl = rawDigitalLifeUV()


class singleDigitalLifeUV:
    def __init__(self, data, exportImgTypes: list = ['tif', 'png']) -> None:
        if isinstance(data, str):
            data = self._fromCfg(file=data)
        if isinstance(data, dict):
            data = DotDict(data)
        if not isinstance(data, (rawDigitalLifeUV, DotDict)):
            return
        self.nameCN = Filter.cutoff(
            Filter.onlyCN(data.nameCN, DEFAULT_NAME_CN), 4)
        self.nameEN = Filter.onlyASCII(data.nameEN, _get_pinyin(self.nameCN))
        self.birthDate = Filter.equelLength(Filter.onlyASCII(
            data.birthDate, DEFAULT_BIRTH_DATE), DEFAULT_BIRTH_DATE)
        self.trCode = Filter.equelLength(Filter.onlyASCII(
            data.trCode, DEFAULT_TOP_RIGHT_CODE), DEFAULT_TOP_RIGHT_CODE)
        self.barCode = Filter.cutoffandComplete(Filter.onlyASCII(
            data.barCode, DEFAULT_TOP_RIGHT_CODE), 18, '-')
        self.snCode = Filter.cutoff(
            Filter.onlyASCII(data.snCode, DEFAULT_SN_CODE), 20)
        self.basePNG = data.basePNG

        # private parameters
        self._exportImgTypes = exportImgTypes
        self._barcodeTmpDir = BARCODE_TEMP_DIR
        # self._outputPath=outputPath
        pass

    @classmethod
    def from_cli(self):
        nameCN = input(
            f'输入名字，最多四个字，仅截取中文，默认为{DEFAULT_NAME_CN}：') or DEFAULT_NAME_CN

        nameEN = _get_pinyin(Filter.cutoff(nameCN, 4))
        if input(f'\n名字拼音为：{nameEN}\n是否修改输入拼音/英文名？\n输入y进入手动输入，不输入或输入其他跳过\n') == 'y':
            nameEN = input("\n输入名字拼音或英文名。支持ASCII字符：\n").upper()
        print(f'英文名已经设置为：{nameEN}')

        birthDate = input(
            f'\n输入生日，示例：{DEFAULT_BIRTH_DATE}：\n') or DEFAULT_BIRTH_DATE

        barCode = input(
            "\n输入条形码内容，\n 格式为18个非中文字符\n输入__UUID__可以自动生成18位随机字符\n也可以输出自定义输入，少于18位会自动使用 - 填补\n").ljust(18, '-')  # 条形码内容
        if barCode.upper() == BARCODE_UUID_ENABLE_KEY.ljust(18, '-'):
            barCode = ''.join(str(uuid.uuid1(clock_seq=18)).split('-'))[:18]
        print(f'条形码已经设置为：{barCode}')

        trCode = input(
            "\n顶部年份，固定四位\n也可自定义为其他四位短语，仅支持非中文字符\n，示例：1900，CM02等：\n")  # 顶部年份

        snCode = input(
            "\n输入自定义sn码\n不输入即为默认(PN-R-DSM01 A513C)\n") or DEFAULT_SN_CODE  # 生日

        return singleDigitalLifeUV(rawDigitalLifeUV(nameCN, nameEN, birthDate, trCode, barCode, snCode))

    def export(self, suffix: str = '', outputPath='./output/', filenameOveride=None):
        assert suffix in ['tif', 'png', 'json',
                          ''], "illegal output file type !"
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
        _font = DEFAULT_FONTFAMILY.CN_l if _islongname else DEFAULT_FONTFAMILY.CN
        draw.text(xy=(580, 1000 + _islongname*10), text=self.nameCN,
                  fill=(255, 255, 255), font=_font)
        # # 添加姓名拼音加日期
        _top_left_str = " ".join(re.findall(
            ".{1}", self.nameEN + '-A' + self.birthDate))
        draw.text(xy=(2440 - len(_top_left_str) * 38, 142),
                  text=_top_left_str, fill=(255, 255, 255), font=DEFAULT_FONTFAMILY.topEN)
        # 添加顶部后边的年份
        draw.text(xy=(2515, 120), text=self.trCode, fill=(
            255, 255, 255), font=DEFAULT_FONTFAMILY.trCode)
        # 添加条码上的文字
        draw.text(xy=(2705 - len(self.snCode) * 40, 1010), text=self.snCode,
                  fill=(255, 255, 255), font=DEFAULT_FONTFAMILY.snCode)
        # 添加条码
        b_code_img = self._gen_barcode(self.barCode, self._barcodeTmpDir)
        img.paste(b_code_img, (1380, 1110))
        return img

    def _imgsavewarpper(self, img: Image, filename: str):
        try:
            img.save(f'{filename}')
            print(f'\n{filename} 生成成功！')
        except:
            print(f'\n{filename} 生成失败！\n')

    @staticmethod
    def _fromCfg(file: str) -> rawDigitalLifeUV:
        return

    @staticmethod
    def _gen_barcode(text, barcodeTmpDir=BARCODE_TEMP_DIR):
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
        if isinstance(data, str):
            self.data = self.readfromCSV(data)
            return
        assert isinstance(data, list), 'date Type error'
        self.data = {idx+1: {'dl': dl, 'orderedID': idx+1} for idx,
                     dl in enumerate(data) if isinstance(dl, singleDigitalLifeUV)}
        pass

    def export(self, suffix: str = '', outputPath='./output/'):
        for id, dl in self.data.items():
            dl['dl'].export(suffix=suffix, outputPath=outputPath,
                            filenameOveride=dl['orderedID']+'_'+dl['dl'].nameCN)

    @staticmethod
    def readfromCSV(filename):
        import csv
        data = {}
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # print(row)
                ordered_id = row[Filter.titleMap_DL2CSV('orderID')]
                otherCommit = row[Filter.titleMap_DL2CSV('otherCommits')]
                _uuid = str(base64.b64encode((row[Filter.titleMap_DL2CSV(
                    'submitTime')] + row[Filter.titleMap_DL2CSV('submitUser')]).encode('utf-8')), 'utf-8')
                # data = {Filter.titleMap_DL2CSV(i):row[Filter.titleMap_DL2CSV(i)] for i in }
                # d = DEFAULT_DL._asdict()
                d = {k: row[Filter.titleMap_DL2CSV(
                    k)] for k, _ in default_dl._asdict().items() if k != 'basePNG'}
                d['basePNG'] = BASE_IMAGE
                data[_uuid] = {'dl': singleDigitalLifeUV(
                    d), 'orderedID': ordered_id}
        return data
