import datetime

import schedule
import time
import os
import logging

import requests
from lxml import etree

# 参数
params = {
    "categories": "010",
    "purity": "110",
    "sorting": "date_added",
    "order": "desc",
    "page": "1",
}

# 创建photoFolder文件夹
if not os.path.exists("photoFolder"):
    os.mkdir("photoFolder")

# 打印日志级别
lft = "%(asctime)s-%(levelname)s-%(message)s-%(lineno)d"
dft = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.INFO, format=lft, datefmt=dft)

# 切换到photoFolder文件夹
os.chdir("photoFolder")


# 获取网页源码
def get_photo():
    date = str(datetime.datetime.now().date())
    if not os.path.exists(date):
        os.mkdir(date)
    for page in range(1, 17):
        params["page"] = str(page)
        res = requests.get("https://wallhaven.cc/search", params=params).text
        tree = etree.HTML(res)
        list1 = tree.xpath('//*[@id="thumbs"]/section[1]/ul/li')
        for item in list1:
            try:
                logging.info("开始下载")
                url = item.xpath('./figure/a[1]/@href')[0]
                res2 = requests.get(url).text
                tree2 = etree.HTML(res2)
                # 获取图片地址
                photoUrl = tree2.xpath('//*[@id="wallpaper"]/@src')[0]
                fileName = photoUrl.rsplit("/", 1)[1]
                if os.path.exists(date+"/"+fileName):
                    logging.info(fileName + "已存在")
                    continue
                # 下载图片
                photo = requests.get(photoUrl)
                with open(date+"/"+fileName, "wb+") as f:
                    f.write(photo.content)
                    f.flush()
                    logging.info(fileName + "下载完成")
                # 每下载一张图片休眠10秒
                time.sleep(10)
            except Exception as e:
                logging.error(e)
                continue


# 每天00:00执行get_photo函数
schedule.every().day.at("00:00").do(get_photo)

if __name__ == '__main__':
    logging.info("开始执行")
    while True:
        schedule.run_pending()
        time.sleep(1)
