# pdfdir —— PDF导航书签添加工具

[![Build Status](https://travis-ci.org/chroming/pdfdir.svg?branch=master)](https://travis-ci.org/chroming/pdfdir)

**已支持子目录功能。**

**已支持Windows/macOS/Ubuntu三平台。**

根据已有的目录文本为你的PDF自动生成导航书签。

![pdfdir](https://user-images.githubusercontent.com/9926275/29554882-5ea72db8-8753-11e7-9667-fe71e00b9c58.png)

*此项目实现逻辑深受 https://github.com/ifnoelse/pdf-bookmark 项目影响。*

## 软件功能

根据网上或PDF中已有的目录内容自动将导航书签插入PDF文件中。

适用于以下场景：

1. 扫描版电子书籍无导航书签；
2. 文字版电子文档无导航书签但PDF中有目录。

## 下载

Windows/macOS/Ubuntu:

[下载地址](https://github.com/chroming/pdfdir/releases)

其他平台：

请使用[源码方式](#通过源码运行)运行或自行打包。

## 基本用法

### 使用

+ 选择文件（必填）：在 "PDF文件路径" 文本框中填入pdf文件路径（如D:/统计思维.pdf）或点击 "打开" 按钮通过文件管理器选择所需的pdf文件。
+ 目录文本（必填）：将目录文本粘贴到“目录文本”框中。[如何获取目录文本](#获取目录文本)。
+ 偏移页（默认0）：指实际页数与文档内容下标页码的差值，如：第一章实际在pdf的第5页，但此页的下标页码为第1页，则偏移页为4 。
+ 子目录区域（非必填区域）：
  + 首层：用于匹配最外层目录标题的[正则表达式](#正则表达式简要说明)，勾选启用。
  + 二层：用于匹配首层子目录标题的正则表达式。
  + 三层：用于匹配二层子目录标题的正则表达式。
  + 未识别：前三层表达式都未匹配到的标题当作第几层。默认当作首层。
+ 写入导航：前三个均填好之后就可以点击 "写入导航" 自动将目录写入pdf的新拷贝中，拷贝文件自动命名为 "原文件名_new.pdf"。

###  获取目录文本

目录文本是类似以下形式的文本内容：

```
中译版序言
致中国读者
作者来信
前言
第1章社会心理学导论2
第一编社会思维
第2章社会中的自我32
.....................
结语605
参考文献606
```

即：*标题+页数*形式。文本内容一般来源于网上书店（如亚马逊）或图书介绍网站（如豆瓣读书）。图书的介绍中一般会列出该书的目录文本，如亚马逊的在 *商品描述--目录* 下。注意：自动生成的目录完全依赖于目录文本，如果此文本有问题则生成的目录也会有问题。

### 英文支持

下载源码中的language/en.qm 放到程序同目录下 language/en.qm , 之后点击程序菜单栏中的 "语言 -- English" 即可切换为英文界面。

### 已知问题

+ 一般图书非正文部分（如序言，目录等）没有标页码或使用另一套页码标记，本程序将这些目录默认链接到第一页，如需修正这些链接可手动修改。
+ 有些正文中的目录没有标页码，程序会将该条目录链接到上一个有页码的标题页。

## 其他

### 通过源码运行

运行源码所需环境：

+ Python2/3 均可，推荐Python3
+ PyQt5
+ PyPDF2
+ six

*注意：Python2与Python3 不兼容，某些系统（如macOS）系统自带Python2，使用`python`命令调用，若自行安装Python3则可能需要通过`python3`来调用Python3，pip同理。本文不区分python/python3, pip/pip3，请用户按当前系统所安装版本使用对应命令。*

#### 获取代码

`git clone https://github.com/chroming/pdfdir`

#### 安装运行环境

安装Python:

https://www.python.org/downloads/

安装依赖包:

进入项目目录，执行：

`pip install -r requirements.txt`

`pip install -r pyqt5`

若提示`No matching distribution found for pyqt5` 可参照[PyQt官方文档](http://pyqt.sourceforge.net/Docs/PyQt5/installation.html)进行安装。

环境装好之后进入源码目录，运行以下命令：

`python run_gui.py`

如果不需要GUI界面:

`python run.py`

### 打包源码

如果你想在本机打包此程序：

安装Pyinstaller

`pip install pyinstaller`

打包程序

`pyinstaller.py -F run_gui.py -n "PDFdir.exe"  --noconsole`


### 目录文本格式

目前通过以下格式处理目录文本：

*标题+页数+换行符*

所有在一行的都被认为是一条目录。页数通过正则`(\d*$)`匹配（匹配文本结尾处的所有数字），如果匹配不到则默认为第一页或上一条目录的页数。

### 正则表达式简要说明

正则表达式是编程中常用的一种工具。如果你没有使用过，可以把他当成类似于office中通配符的东西。
本工具中可能会用到的正则：
+ \d 表示单个数字，如 "第\d章" 可以匹配 "第1章", "第2章"……等，但不能匹配"第10章", 因为10是两个数字；
+ \w 表示单个字符，包括单个数字。如 "第\w章" 可以匹配"第1章", "第一章"……等；
+ . 表示任意字符，包括\w所能匹配的所有字符以及空格等特殊字符；
+ \* 表示表达式中的前一个符号可以匹配不到，或匹配任意多次，如 "第\d*章" 可以匹配 "第章", "第1章", "第100章"； 
+ \+ 跟\*类似，但是前一个符号不能匹配不到；
+ {m, n} 匹配前一个字符m至n次。


注意：

+ \*, \+ 符号会匹配尽可能多的内容，比如如果用"第\w\*章" 来匹配，"第一节如何阅读此章"这段内容也会被匹配到，更好的写法是确定要匹配内容的长度，写成"第\w{1,2}章"。
+ 要匹配一个不是正则表达式中的正常字符直接写即可，如"第", "1", 甚至包括空格。但正则表达式中有定义用于匹配的一些特殊字符如果要作为普通字符匹配，则要在前面加一个"\\"，比如匹配"1.1"这种格式，可以写成"\d\\.\d"。"\\"符号本身也要如此。

