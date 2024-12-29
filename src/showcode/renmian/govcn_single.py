import re
from collections import namedtuple
from datetime import datetime
from pathlib import Path, PurePath
from urllib.request import Request, urlopen

import pandas as pd
from bs4 import BeautifulSoup

RenMian = namedtuple(
    "RenMian",
    "文号, 日期, 任免, 姓名, 职务",
    defaults=["", datetime(1, 1, 1), True, "", ""],
)


def save_links(urlset):
    k = 0
    for url in urlset:
        print(k, "次: ", url)
        save_f = PurePath(url.split("/", maxsplit=3)[-1])
        Path(save_f.parent).mkdir(0o755, True, True)

        read_url = Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
            },
        )

        with urlopen(read_url) as f:
            response = f.read().decode("utf-8")

        # 政府网网页源码有错误，出现两次</html> 标签。会导致bs4解析到第一个标签时停止。
        response = response.replace("</html>", "", 1)
        Path(save_f).write_text(response)


def htm_parse(topdir, suffix):

    p = Path(topdir)
    filelist = p.glob("**/" + suffix)
    tuple_all = []

    for i in filelist:
        response = i.read_text()
        soup = BeautifulSoup(response, "lxml")

        wenhao = soup.select_one("#lastNodeID")
        wenhao = wenhao.getText() if wenhao is not None else "error"

        # 主页面的css-selecotr是#UCAP-CONTENT
        contents = soup.select_one("#UCAP-CONTENT")
        if contents is None:
            continue

        times, main_str = pattern(contents.getText(strip=True))
        if times is None or main_str is None:
            print("Some eror in: ", i.resolve())
            continue

        list1 = process(wenhao, times, main_str)
        tuple_all += list1
    return tuple_all


def pattern(contents_main):
    times = re.findall(r"\d+年\d+月\d+日", contents_main)
    renmian_content = re.split(r"\d+年\d+月\d+日", contents_main)

    # content应该最少包括日期之前的部分和日期之后的部分
    if len(times) == 0 or len(renmian_content) <= 1:
        return None, None

    renmian_content.pop(0)
    return times, renmian_content


def process(wenhao, times, renmian_content):

    lst = []

    if times is None or renmian_content is None:
        return lst
    # 此外网站上还有 '不再兼任','不再担任' 等字样，因涉及数据极少， 在此忽略不计
    re_renmian = re.compile(
        r"任命([^，。；]*?)为[^，。；]*?，免去其([^，；。]*?)职务[，；。]"
    )
    re_ren = re.compile(r"任命([^，。；]*?)[为兼]([^，；。]*?)[，；。]")
    re_mian = re.compile(r"免去(?!其)([^，。；]*?)的([^，。；]*?)职务[，；。]")

    for i in range(len(times)):
        ren_date = datetime.strptime(times[i], "%Y年%m月%d日")
        strs = renmian_content[i]
        for name, zhiwu in re_renmian.findall(strs):
            lst.append(RenMian(wenhao, ren_date, False, name, zhiwu))
        for name, zhiwu in re_ren.findall(strs):
            lst.append(RenMian(wenhao, ren_date, True, name, zhiwu))
        for name, zhiwu in re_mian.findall(strs):
            lst.append(RenMian(wenhao, ren_date, False, name, zhiwu))
    return lst


def renmian_df(tuples):
    df = pd.DataFrame.from_records(
        tuples, columns=["文号", "日期", "任免", "姓名", "职务"]
    )

    df = df.assign(姓名=df["姓名"].str.split("、")).explode("姓名")
    df = df.assign(职务=df["职务"].str.split("、")).explode("职务")

    df_ren = df[df["任免"] == True]
    df_ren = df_ren.drop(columns="任免")
    df_ren.rename(columns={"日期": "任职日期"}, inplace=True)

    df_mian = df[df["任免"] == False]
    df_mian = df_mian.drop(columns="任免")
    df_mian.rename(columns={"日期": "免职日期"}, inplace=True)
    df = df_ren.merge(df_mian, how="outer")

    new_order = ["姓名", "职务", "任职日期", "免职日期", "文号"]
    df = df[new_order]
    print("汇总表统计： ")
    df.info()
    print("\n\n")
    df.to_excel("renmianhuizong.xlsx", index=False)

    df.drop(columns="文号", inplace=True)
    df1 = df[["姓名", "职务", "任职日期"]]
    df1 = df1.dropna()
    df2 = df[["姓名", "职务", "免职日期"]]
    df2 = df2.dropna()

    df = df1.merge(df2, how="outer")
    df["在职时长"] = df["免职日期"] - df["任职日期"]

    print("合表统计： ")
    df.info()
    print("\n\n")

    df.to_excel("renmianhe.xlsx", index=False)

    # 有些官员因多次任免同一职务，会导致在职时长为负数，影响统计，因此去掉。
    df = df[df["在职时长"] > pd.Timedelta(days=0)]
    print("在职时长统计： ", df["在职时长"].describe())


def from_pickle(filename):
    if not Path(filename).exists():
        return None

    import pickle

    # TODO: 有空时再做 可增补更新 的任免表。
    with open(filename, "rb") as f:
        url_set = pickle.load(f)
    return url_set


if __name__ == "__main__":
    filename = "urlset.dat"
    url_set = from_pickle(filename)
    save_links(url_set)

    tuples = htm_parse("./gongbao", "*.htm")
    renmian_df(tuples)
