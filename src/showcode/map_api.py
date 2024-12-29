"""通过百度和高德地图api查询地址的坐标信息

Examples:
    查询某一地址的坐标::

        address1 = ret_bai_gps('复圣公园', '宁阳')
        address2 = ret_gao_gps('复圣公园', '泰安')
        print(f'baidu gps: {address1}\tgaode gps: {address2}')

        # 统一获取excel文件中的'生产经营单位名称'列，并添加坐标经纬度和精度::
        import pandas as pd

        df = pd.read_excel('/home/sd44/111.xlsx')

        df['baidu address'] = df['生产经营单位名称'].map(lambda x: ret_bai_gps(x, '宁阳'),
                                                na_action='ignore')
        print(f"{df['baidu address']}")
        df[['bai_lng', 'bai_lat',
            'bai_compress']] = df['baidu address'].str.split(';', expand=True)
        df.drop(columns='baidu address')

        df['gaode address'] = df['生产经营单位名称'].map(lambda x: ret_gao_gps(x, '泰安'),
                                                na_action='ignore')
        df[['gao_lng', 'gao_lat',
            'gao_compress']] = df['gaode address'].str.split(';', expand=True)
        df.drop(columns='gaode address')

        df.head()
        df.to_excel('/home/sd44/2haha.xlsx', index=False)
"""

import json
from urllib import parse
from urllib.request import urlopen

BAIDU_AK = "replace me to your key"
""" BAIDU_AK的值需更改为你自己的百度API KEY """
GAO_AK = "replace me to your key"
""" GAO_AK的值需更改为你自己的高德API KEY """


class Address:
    """存放地址信息

    Attributes:
        name: 地址名称
        is_baidu: 是否百度地图api。高德地图api无法获取精确度，只能将查询范围限制在市级，不能到县级。
        lng: 经度值
        lat: 纬度值
        precise: 是否精确查找（百度地图api独有）
        comprehension: 精确匹配程度（百度地图api独有，值越高越精确。值50时，解析误差100m内概率为79%，误差500m内概率为90%。）
    """

    def __init__(
        self, name, is_baidu=False, lng=0.0, lat=0.0, precise=False, comprehension=0
    ):
        self.name = name
        self.is_baidu = is_baidu
        self.lng = lng
        self.lat = lat
        self.precise = precise
        self.comprehension = comprehension

    def __str__(self):
        return (
            str(self.__class__)
            + "\n"
            + "\n".join(
                (
                    str(item) + " = " + str(self.__dict__[item])
                    for item in sorted(self.__dict__)
                )
            )
        )


def pos_to_bai_coord(name, city):
    """通过百度地图api查询地址坐标值

    百度地图地理编码API详细说明请见
    https://lbsyun.baidu.com/faq/api?title=webapi/guide/webservice-geocoding-base

    Args:
        name: 地址名称
        city: 查询范围，可具体到县级。虽然可以设定查询范围，但不保证返回结果中不超出范围。

    Returns:
        Address
    """
    params = parse.urlencode(
        {
            "address": name,
            "city": city,
            "ak": BAIDU_AK,
            "ret_coordtype": "bd09ll",  # 百度地图默认bd09ll（百度经纬度坐
            # 标），也可以设定为gcj02ll（国测局标准坐标）
            "output": "json",
        }
    )

    baidu_url = f"https://api.map.baidu.com/geocoding/v3/?{params}"

    with urlopen(baidu_url) as f:
        results = f.read().decode("utf-8")
    json_data = json.loads(results)
    # print(json_data)
    if json_data["status"] != 0:
        # print('except status.')
        return Address(name, is_baidu=True, comprehension=-10)

    lng = json_data["result"]["location"]["lng"]
    lat = json_data["result"]["location"]["lat"]
    precise = json_data["result"]["precise"]
    comprehension = json_data["result"]["comprehension"]
    return Address(name, True, lng, lat, precise, comprehension)


def pos_to_gaode_coord(name, city):
    """通过高德地图api查询地址坐标值

    高德地图地理编码API详细说明请见
    https://developer.amap.com/api/webservice/guide/api/georegeo

    Args:
        name: 地址名称
        city: 查询范围，高德地图只能具体到市级。虽然可以设定查询范围，但不保证返回结果中不超出范围。

    Returns:
        Address
    """
    params = parse.urlencode(
        {"address": name, "city": city, "key": GAO_AK, "output": "json"}
    )

    gao_url = f"https://restapi.amap.com/v3/geocode/geo?{params}"

    with urlopen(gao_url) as f:
        results = f.read().decode("utf-8")
    json_data = json.loads(results)
    if json_data["status"] != "1":
        print(f'ERROR: {json_data["info"]}')
        return Address(name, False, comprehension=-10)
    lng, lat = (json_data["geocodes"][0]["location"]).split(",")
    level = json_data["geocodes"][0]["level"]

    comprehension = 50
    bad_compre = ["市", "区县", "乡镇"]
    if (
        level in bad_compre
    ):  # 只能精确到乡镇级的话，精度太差，误差太大，设定comprehension为 -10
        comprehension = -10

    return Address(name, False, float(lng), float(lat), comprehension=comprehension)


def ret_bai_gps(name, city="宁阳"):
    """通过百度API获取地址名称的经纬度和精度

    Args:
        name: 地址名称
        city: 查询范围，可具体到县级。虽然可以设定查询范围，但不保证返回结果中不超出范围。

    Returns:
        gps字符串，如'166.2424,35.23424'
    """
    address = pos_to_bai_coord(name, city)
    return f"{address.lng};{address.lat};{address.comprehension}"


def ret_gao_gps(name, city="泰安"):
    """通过高德API获取地址名称的经纬度和精度

    Args:
        name: 地址名称
        city: 查询范围，可具体到县级。虽然可以设定查询范围，但不保证返回结果中不超出范围。

    Returns:
        gps字符串，如'166.2424,35.23424'
    """
    address = pos_to_gaode_coord(name, city)
    return f"{address.lng};{address.lat};{address.comprehension}"
