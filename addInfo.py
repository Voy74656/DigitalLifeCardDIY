# coding=UTF-8
import re
import uuid

from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter as bcWriter

from xpinyin import Pinyin

EnFont = ImageFont.truetype(font="./necessary fonts/DINPro-Medium.otf")
EnTopFont = ImageFont.truetype(
    font="./necessary fonts/DINPro-Medium.otf", size=70)
EnTopYEARFont = ImageFont.truetype(
    font="./necessary fonts/HarmonyOS_Sans_SC_Bold.ttf", size=120)
ChFont = ImageFont.truetype(
    font="./necessary fonts/HarmonyOS_Sans_SC_Regular.ttf", size=220)
ChSNTextFont = ImageFont.truetype(
    font="./necessary fonts/HarmonyOS_Sans_SC_Medium.ttf", size=80)
ChFontForLong = ImageFont.truetype(
    font="./necessary fonts/HarmonyOS_Sans_SC_Regular.ttf", size=200)
en_regex = re.compile(r'[0-9a-zA-z]')
ch_regex = re.compile(r'[\u4E00-\u9FA5]')
pinyin = Pinyin()

BARCODE_UUID_ENABLE = '__UUID__'

DEFAULT_NAME_CN = '图丫丫'

DEFAULT_NAME_EN = ''

DEFAULT_BIRTH_DATE = '19000101'

DEFAULT_PN_CODE = 'PN-R-DSM01 A513C'

DEFAULT_BARCODE = ''.join(str(uuid.uuid1(clock_seq=18)).split('-'))[:18]

DEFAULT_YEAR = '2023'


def make_tif(path):
    with open(path, "rb") as f:
        png = Image.open(fp=f)
        png.save(path.replace("png", "tif"))


def gen_barcode(text):
    '''
    生成条形码
    '''
    b = barcode.get("code128", text, writer=bcWriter())
    b.save('./output/barcode')
    with open("./output/barcode.png", "rb") as f:
        barcodeimg = Image.open(fp=f)
        barcodeimg = barcodeimg.crop((20, 20, 600, 50))
        barcodeimg.save("./output/barcode_crop.png")
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
        barcodeimg.save("./output/barcode_bin.png")
        return barcodeimg


def add_one(name, name_EN, birth, my_year, SN, sn_text, img):
    draw = ImageDraw.Draw(img)
    # 简单处理下数据输入的有效性
    if len(name) > 4:
        name = name[0:4]

    if len(birth) != 8:
        birth = "19000101"

    if len(SN) > 18:
        SN = SN[0:18]
    if len(SN) < 18:
        SN = SN.ljust(18, "-")

    if len(sn_text) > 20:
        sn_text = sn_text[0:20]
    if len(sn_text) == 0 or sn_text.isspace():
        sn_text = "PN-R-DSM01 A513C"

    if len(my_year) != 4:
        my_year = "2023"

    sn_text = sn_text.upper()

    nameFont = ChFont
    y = 1000
    if len(name) > 3:
        nameFont = ChFontForLong
        y = 1010

    # 添加姓名
    draw.text(xy=(580, y), text=name, fill=(255, 255, 255), font=nameFont)
    # if name_EN != '':
    #     name_EN = name_EN
    # else:
    #     name_EN = pinyin.get_pinyin(name, splitter='', convert='upper')
    top_left_str = name_EN + '-A' + birth

    text_list = re.findall(".{1}", top_left_str)
    new_top_left_str = " ".join(text_list)
    # 添加姓名拼音加日期
    draw.text(xy=(2440 - len(new_top_left_str) * 38, 142),
              text=new_top_left_str, fill=(255, 255, 255), font=EnTopFont)
    # draw.text(xy=(2440 - len(new_top_left_str) * 38, 142), text="Benie-Y20080210", fill=(255, 255, 255), font=EnTopFont)
    # 添加顶部后边的年份
    draw.text(xy=(2515, 120), text=my_year, fill=(
        255, 255, 255), font=EnTopYEARFont)

    # 添加条码上的文字
    draw.text(xy=(2705 - len(sn_text) * 40, 1010), text=sn_text,
              fill=(255, 255, 255), font=ChSNTextFont)

    b_code_img = gen_barcode(SN)
    img.paste(b_code_img, (1380, 1110))


'''
条形码内容，必须为18个非中文字符，不够用 - 填补
比如    "HandsomeJack"
填补成  "HandsomeJack------"
'''


def single_test():
    my_name = input("输入名字，最多四个字，默认为图丫丫：") or DEFAULT_NAME_CN # 名字,最多四个字，再多不支持了
    my_name_EN = pinyin.get_pinyin(my_name, splitter='', convert='upper')

    my_name_EN = DEFAULT_NAME_EN

    if my_name_EN == '' and input(f'\n名字拼音为：{my_name_EN}\n是否手动输入拼音/英文名？\n输入y进入手动输入，不输入或输入其他跳过\n') == 'y':
        my_name_EN = input("\n输入名字拼音或英文名。支持非中文字符：\n").upper()

    my_birth = input("\n输入生日，示例：19000101：\n")  # 生日

    barcode_text = input(
        "\n输入条形码内容，\n 格式为18个非中文字符\n输入__UUID__可以自动生成18位随机字符\n也可以输出自定义输入，少于18位会自动使用 - 填补\n").ljust(18, '-')  # 条形码内容
    if barcode_text == BARCODE_UUID_ENABLE.ljust(18, '-'):
        barcode_text = DEFAULT_BARCODE
    print(f'条形码已经设置为：{barcode_text}')

    my_year = input("\n顶部年份，固定四位\n也可自定义为其他四位短语，仅支持非中文字符\n，示例：1900，CM02等：\n")  # 顶部年份

    my_sn_text = input("\n输入自定义pn码\n不输入即为默认(PN-R-DSM01 A513C)\n")  # 生日

    with open(f'水贴底图 4K B.png', 'rb') as f:
        BaseImg = Image.open(fp=f)
        img = BaseImg.copy()
        add_one(my_name, my_name_EN, my_birth,
                my_year, barcode_text, my_sn_text, img)
        img.save("./output/%s.png" % (my_name))
        make_tif("./output/%s.png" % (my_name))
    pass


def batch_gen():
    return ''


if __name__ == "__main__":
    single_test()
