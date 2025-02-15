# -*- coding: utf-8 -*-

"""Convert a directory text which from website to index dict"""

import re


def split_page_num(text):
    """split between title and page number"""
    text = text.strip()
    con, num = re.search(r"(.*?)((?<!-)-?\d+$|\d*$)", text).groups()
    if con:
        con = con.rstrip(' .-')
    if num == '':
        num = 1
    return con, int(num)


def text_to_list(text):
    if isinstance(text, list):
        return text
    return text.splitlines()


def is_in(title, exp):
    try:
        return bool(re.match(exp, title)) if exp else False
    except Exception as e:
        print("Check regex error! %s" % e)


def check_level(title, level0, level1, level2, level3=None, level4=None, level5=None, other=0):
    """check the level of this title"""
    ls = [level0, level1, level2, level3, level4, level5]
    for i in range(len(ls)):
        idx = len(ls)-1 - i  # reserve match
        if is_in(title, ls[idx]):
            return idx
    # no level found
    return other


def _convert_dir_text(dir_text, offset=0, level0=None, level1=None, level2=None, level3=None, level4=None, level5=None, other=0):
    l0, l1, pagenum, index_dict = 0, 0, -float("inf"), {}
    l2, l3, l4 = 0, 0, 0
    dir_list = text_to_list(dir_text)
    i = 0
    for di in dir_list:
        title, num = split_page_num(di)
        if num > pagenum:
            pagenum = num
        index_dict[i] = {'title': title, 'real_num': pagenum+offset, 'num': pagenum}
        level = check_level(title, level0, level1, level2, level3, level4, level5, other=other)
        if level == 5 and i != l4:
            index_dict[i]['parent'] = l4
        elif level == 4 and i != l3:
            index_dict[i]['parent'] = l3
            l4 = i
        elif level == 3 and i != l2:
            index_dict[i]['parent'] = l2
            l3 = i
        elif level == 2 and i != l1:
            index_dict[i]['parent'] = l1
            l2 = i
        elif level == 1 and i != l0:
            index_dict[i]['parent'] = l0
            l1 = i
        elif level == 0:
            l0 = i
        i += 1
    return index_dict


def convert_dir_text(dir_text, offset=0, level0=None, level1=None, level2=None, level3=None, level4=None, level5=None, other=0):
    """
    convert directory text to dict.

    :param: dir_text: unicode, the directory text, usually copy from a bookstore like amazon.
    :param: offset: int, the offset of this book.
    :param: level0: unicode, the expression to find level0 title.
    :param: level1: unicode, the expression to find level1 title.
    :param: level2: unicode, the expression to find level2 title.
    :param: level3: unicode, the expression to find level3 title.
    :param: level4: unicode, the expression to find level4 title.
    :param: level5: unicode, the expression to find level5 title.
    :param: other: unicode, three level can't match title, then this is the level.
    :return: the dict of directory, like {0:{'title':'A', 'pagenum':1}, 1:{'title':'B', pagenum:2, parent: 0} ......}

    """
    return _convert_dir_text(dir_text, offset, level0, level1, level2, level3, level4, level5, other=other)
