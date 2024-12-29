#!/usr/bin/env python3
"""将某一目录下（包括子文件夹）的所有excel文件汇总合并为一个excel xlsx文件

Example:
    将 ``/home/sd44/ri`` 文件夹下的所有excel文件合并到 ``/home/sd44/xx.xlsx``
    ::

        process_pipline('/home/sd44/ri', '/home/sd44/xx.xlsx')


"""

import itertools
import sys
from pathlib import Path

import pandas as pd


def gen_find(filepat, topdir):
    """Find all filenames in a directory tree that match a shell wildcard pattern

    Args:
        filepat: string, 通配符后缀名，如 ``'*.jpeg'``
        topdir: 递归查找的顶级目录

    Returns:
        匹配到的文件Path生成器
    """
    p = Path(topdir)
    return p.glob("**/" + filepat)


def gen_opener(filenames):
    """获取所有excel文件内容并yield

    Open a sequence of filenames one at a time producing a file object.
    The file is closed immediately when proceeding to the next iteration.

    Note:
        ``pd.read_excel`` 函数参数请根据实际情况酌情修改。碍于时间关系，不再分解。

    Args:
        filenames (generator(str)): 文件名列表

    Returns:
        generator(DataFrame) : 所有excel文件中所有sheet的DataFrame
    """
    for filename in filenames:
        if str(filename).startswith("~"):
            continue  # 不包括临时文件（非完整excel格式）

        df_dict = pd.read_excel(filename, header=None, index_col=None, sheet_name=None)
        if isinstance(df_dict, dict):
            for sheet_name, df in df_dict.items():
                df["filename"] = (
                    str(filename) + " " + sheet_name
                )  # 添加文件名列，方便debug
                yield df
        else:
            print(f"Read excel file error:{filename}", file=sys.stderr)


def process_pipline(path, write_file):
    xlsx_files = gen_find("*.xlsx", path)
    xls_files = gen_find("*.xls", path)
    files = itertools.chain(xlsx_files, xls_files)

    dfs = (i for i in gen_opener(files))
    df = pd.concat(dfs, axis=0, ignore_index=True)
    df.dropna(axis="index", how="all", inplace=True)
    # df.drop_duplicates(inplace=True) # 删除重复行，因为前面加入了 filename列。,实际上可去除的很少.如果不加filename列的话，效果显著
    print(df)
    df.to_excel(write_file, index=False, header=False)
