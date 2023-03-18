# 数字生命卡水贴生成


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

pip 是一个现代的，通用的 Python 包管理工具。提供了对 Python 包的查找、下载、安装、卸载的功能。

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
git clone https://gitee.com/voy74656/xxxx.git
```

### 安装项目依赖

在项目目录下打开控制台，执行以下命令安装项目依赖（默认使用[清华大学tuna镜像源](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/)）
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirement.txt
```

### 生成自定义生命卡水贴
使用python执行脚本，根据交互命令进行自定义
```bash
python addInfo.py
