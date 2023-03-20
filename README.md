# 数字生命卡水贴生成

示意图1：（透明背景白色图案，请点击查看）

![image](output/爱莉希雅.png)

示意图2：（透明背景白色图案，请点击查看）

![image](水贴成品%204K%20A.png)

## 使用准备

### 前提：python环境安装和pip安装

`linux`下自带python环境，如在`windows`下使用，请参考`windows`下安装`python`的相关教程

[知乎@津野|全网最详细的Python安装教程（Windows）](https://blog.csdn.net/qq_44214671/article/details/113469811)

如在CMD/POWERSHELL/Bash 中执行`python -V`或`python3 -V`，有类似输出，即证明python环境正常

```bash
voy74656@Dell-G15-5515:~$ python3 -V
Python 3.10.6
```

**检查pip安装**

> pip 是一个现代的，通用的 Python 包管理工具。提供了对 Python 包的查找、下载、安装、卸载的功能。

在正式安装pip之前，可在CMD/POWERSHELL/Bash输入以下命令，用于检测当前Windows环境中是否已经安装pip。

```bash
python -m pip --version
```

以下是一个样例输出，如输出结果类似，即证明pip已安装，可以进行下一步

```bash
voy74656@Dell-G15-5515:~$ python3 -m pip --version
pip 23.0.1 from /usr/local/lib/python3.10/dist-packages/pip (python 3.10)
```

### 下载本项目

对未安装`git`的windows用户，请直接下载本项目zip文件，并解压

已安装git，执行如下命令

``` bash
git clone https://gitee.com/Voy74656/DigitalLifeCardDIY.git
```

### 安装项目依赖

在**项目目录**下打开控制台，执行以下命令安装项目依赖（默认使用[清华大学tuna镜像源](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/)）

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirement.txt
```

## 使用方法

参照帮助

```bash
voy74656@Dell-G15-5515:~/workspace/DigitalLifeCardDIY$ python3 ./generator.py --help
USAGE:

    python /home/chengys/workspace/DigitalLifeCardDIY/generator.py [opt]

opts:
        -c / --cil:                   (DEFAULT) Generate DigitalLife Card UV in console.
        -g / --group [csv file]:      Auto generate DigitalLife Card UVs for group.
        -o / --output [output path]:  Set output dir, can work with -c and -g command
                                      Dafault: ./output/
        -v / --version:               Display script version & developer's information
        -h / --help:                  Display this help file
```

### 1. 命令行交互式生成自定义生命卡水贴

即使不使用输入参数，使用python执行脚本，即可根据交互命令进行自定义

```bash
python generator.py 
```

以下是一个样例

```bash
voy74656@Dell-G15-5515:~/workspace/DigitalLifeCardDIY$ python generator.py 
输入名字，最多四个字，默认为图丫丫：爱莉希雅

名字拼音为：AILIXIYA
是否手动输入拼音/英文名？
输入y进入手动输入，不输入或输入其他跳过
y

输入名字拼音或英文名。支持非中文字符：
EGO-ALYSIA

输入生日，示例：19000101：
20211111

输入条形码内容，
 格式为18个非中文字符
输入__UUID__可以自动生成18位随机字符
也可以输出自定义输入，少于18位会自动使用 - 填补
__UUID__
条形码已经设置为：cb88ef4bc58911ed80

顶部年份，固定四位
也可自定义为其他四位短语，仅支持非中文字符
，示例：1900，CM02等：
CM02

输入自定义pn码
不输入即为默认(PN-R-DSM01 A513C)
Miss Pink Elf ~

PNG 生成成功

TIF 生成成功

全部完成
```

样例输出：（透明背景白色图案，请点击查看）

![image](output/爱莉希雅.png)

### 2. 从csv文件中批量读取和生成

```bash
python generator.py -g [csv file] -o [output path]
# -g 选项下需要填写csv文件路径[csv file]，测试样本为./test/demo.csv
# -o 可选设置输出路径，如不选择，[output path]默认为./output/
# csv批量导出的默认命名规则：订单号_定制姓名.png/tif
```

csv文件的结构和表标题如下所示： 

|提交时间（自动）|你需要定制的姓名是？（必填）|你是否需要定制拼音或英文名，需要的话是？|你需要定制的日期是？（必填）|你需要定制的条形码内容是？（必填）|条形码上方编号是？|年份|你的订单号是？（必填）|有什么别的备注？|提交者（自动）|
| :---: | :---: | :---: | :---:| :---: | :---: | :---: | :---: | :---: | :---: |
|2023年3月19日 21:34|爱莉希雅|EOG-ALYSIA|20211111|Elysian Realm CM02|Miss Pink Elf ~|CM02|1234||XXXX|

相应的代码映射请参考`generator.py`中`Filter.titleMap_DL2CSV()`函数的实现与`DigitalLifeUVs.readfromCSV()`的操作

## 文件说明

```bash
Version 2.0
.
├── lib                                                 # 库文件目录
│   ├── __init__.py
│   ├── dataFormat.py
│   ├── defaultConfig.py                                # 默认配置文件，需要修改默认配置可编辑
│   └── utils.py
├── resources                                           # 资源文件夹
│   ├── fonts                                           # 字体文件夹
│   │   ├── DINPro-Medium.otf
│   │   ├── HarmonyOS_Sans_SC_Black.ttf
│   │   ├── HarmonyOS_Sans_SC_Bold.ttf
│   │   ├── HarmonyOS_Sans_SC_Medium.ttf
│   │   └── HarmonyOS_Sans_SC_Regular.ttf
│   ├── 水贴底图 4K B.png                                # 默认底图
│   └── 水贴成品 4K A.png
├── test                                                
│   └── demo.csv                                        # csv输出测试样本文件
├── output                                              # 默认输出文件夹
│   ├── 爱莉希雅.png
│   ├── 爱莉希雅.tif
│   ├── 秦始皇.png
│   └── 秦始皇.tif
├── generator.py                                        # 脚本文件，命令行调用入口
├── README.md                                           # readme 文档（Markdown 格式）
├── readme.txt                                          # readme 文档（Txt 格式）
├── requirement.txt                                     # 项目依赖库列表，可以使用pip管理安装
└── LICENSE                                             # 项目开源协议（MIT）
```
