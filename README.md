# 数字生命卡水贴生成

![image](output/爱莉希雅.png)

![image](水贴成品%204K%20A.png)

## 使用方法

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

### 生成自定义生命卡水贴

使用python执行脚本，根据交互命令进行自定义

```bash
python addInfo.py 
```

以下是一个样例

```bash
voy74656@Dell-G15-5515:~/workspace/DigitalLifeCardDIY$ python addInfo.py 
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

样例输出：
![image](output/爱莉希雅.png)

## 文件说明

```bash
Version 1.0

文件说明
│  addInfo.py                                   // 自动添加信息的python脚本
│  readme.txt
│  数字生命卡.ai                                 // 水贴图的AI格式文件，可以自己打开编辑信息
│  水贴底图4K B.png                              // 导出的4K分辨率底图 B 面底图用于脚本批量生成
│  水贴成品 4K A.png                             // 导出的4K分辨率底图 A 面，大家通用
│
├─necessary fonts                               // 字体文件夹，使用 数字生命卡.AI 文件需要这两个字体
│      DINPro-Medium.otf
│      HarmonyOS_Sans_SC_Regular.ttf
│
└─output
        barcode.png                             // 根据文本生成的条形码，可以扫出信息
        barcode_bin.png                         // 条形码最终水贴图，已经变成白色，无法扫码，仅作对比
        barcode_crop.png                        // 条形码截取图，仅作对比
        刘培茄.png                               // 代码生成的透明图片，以代码中的 my_name 作为文件名，可以拿去创作
        刘培茄.tif                               // 代码生成的文件，以代码中的 my_name 作为文件名，水贴制作需要tif格式
```
