# coding=utf-8
import requests
from bs4 import BeautifulSoup
import os
import random
MockUpNames = [
    {
        'orgName': "Credits",
        'name': "建造金币"
    },
    {
        'orgName': "Timber",
        'name': "木材"
    },
    {
        'orgName': "Balance",
        'name': "维护金币"
    },
    {
        'orgName': "Workforce - farmers",
        'name': "农夫劳动力"
    },
    {
        'orgName': "Attractiveness",
        'name': "吸引力"
    },
    {
        'orgName': "Workforce - jornaleros",
        'name': "临时工劳动力"
    },
    {
        'orgName': "Workforce - workers",
        'name': "工人劳动力"
    },
    {
        'orgName': "Steel beams",
        'name': "钢梁"
    },
    {
        'orgName': "Windows",
        'name': "窗户"
    },
    {
        'orgName': "Reinforced concrete",
        'name': "钢筋混凝土"
    },
    {
        'orgName': "Workforce - engineers",
        'name': "工程师劳动力"
    },
    {
        'orgName': "Workforce - artisans",
        'name': "工匠劳动力"
    },
    {
        'orgName': "Workforce - obreros",
        'name': "劳工劳动力"
    },
    {
        'orgName': "Bricks",
        'name': "砖块"
    }
]

def convertFormat():
    print("程序将会爬取指定页面的数据并转换成灰机建筑表格模板格式")
    location = input("请输入你的Windows用户名: e.g:Administrator")
    print("程序将会在你的桌面上创建一个名为Anno1800 + 当天日期的文件夹")
    pageName = input("请输入页面网址的后缀: url e.g:Production_buildings ")
    path = 'C:\\Users\\' + location + '\\Desktop\\anno1800' + str(random.randint(1,9999)) + '\\'
    if(pageName == 'q'):
        return
    os.mkdir(path)
    formattedText = ""
    url = "https://anno1800.fandom.com/wiki/" + pageName
    r = requests.get(url, stream=True)
    print("正在读取该网址数据：", url)
    soup = BeautifulSoup(r.text, 'lxml')
    for table in soup.find_all("table"):
        formattedText += "{{表格头}}"
        for i in range(2, len(table.findAll('tr'))):
            tr = table.findAll('tr')[i]
            if len(tr.findAll('td')) == 6:
                formattedText += "{{建筑表格模板"
                formattedText += "|名称=" + tr.findAll('td')[1].getText()
                formattedText += "|描述=" + tr.findAll('td')[2].getText()
                formattedText += "|尺寸=" + tr.findAll('td')[5].getText()
                for j in range(3, 5):
                    for k in range(0, len(tr.findAll('td')[j].contents)):
                        if tr.findAll('td')[j].contents[k].name == "a":
                            for item in MockUpNames:
                                if tr.findAll('td')[j].contents[k].contents[0].get("alt") == item['orgName']:
                                    formattedText += "|" + \
                                        item['name'] + "=" + \
                                        tr.findAll('td')[j].contents[k-1]
                formattedText += "|}}"
        formattedText += "{{表格尾}}"
    data=open(path,'w+') 
    print(formattedText,file=data)
    data.close()
    print("转换完成，请删除所有重复{{表格头}}{{表格尾}}。txt文本文件可以在桌面anno1800开头文件夹内找到。")

def downloadImagesFromPage():
    name = input("请输入页面网址的后缀: e.g:Production_buildings ")
    location = input("请输入你的Windows用户名: e.g:Administrator")
    print("加载中...")
    path = 'C:\\Users\\' + location + '\\Desktop\\anno1800' + str(random.randint(1,9999)) + '\\'
    if(name == 'q'):
        return
    os.mkdir(path)
    imageAltList = []
    url = "https://anno1800.fandom.com/wiki/" + name
    r = requests.get(url, stream=True)
    print("正在从以下链接下载Icon...")
    print(url)
    print("加载中...")
    soup = BeautifulSoup(r.text, 'lxml')
    for item in soup.find_all("a", attrs={"class": "image image-thumbnail"}):
        print(item.contents[0].get("alt"))  # image name
        if item.contents[0].get("alt") in imageAltList:
            print("图片已存在，跳过")
        else:
            rImage = requests.get(item.get("href"), stream=True)
            if rImage.status_code == 200:  # if status code is success
                print("读取成功")  # return status code
                imageAltList.append(item.contents[0].get("alt"))
                # write and save image
                open(path + item.contents[0].get("alt") + '.png', 'wb').write(rImage.content)
                print("下载完成，查找下一个...")
            else:
                print("读取失败，状态码：", rImage.status_code)  # return status code
            del rImage
            
        
    print("所有Icon已经下载并位于" + path)

def downloadAllImages():
    print("程序将会下载所有位于anno1800 fandom Iconc页下的icon")
    location = input("请输入你的Windows用户名: e.g:Administrator")
    print("程序将会在你的桌面上创建一个名为Anno1800 + 当天日期的文件夹")
    if location == 'q':
        return
    path = 'C:\\Users\\' + location + '\\Desktop\\anno1800' + str(random.randint(1,9999)) + '\\'
    os.mkdir(path)
    url = "https://anno1800.fandom.com/wiki/Icons"
    r = requests.get(url, stream=True)
    print("正在从以下链接下载Icon...")
    print(url)
    soup = BeautifulSoup(r.text, 'lxml')
    for item in soup.find_all("a", attrs={"class": "image lightbox"}):
        print(item.get("href"))  # image link
        print(item.contents[1].get("alt"))  # image name
        rImage = requests.get(item.contents[1].get("data-src"), stream=True)
        print(rImage.status_code)  # return status code
        if rImage.status_code == 200:  # if status code is success
            # write and save image
            open(path + item.contents[1].get("alt") +
                 '.png', 'wb').write(rImage.content)
        del rImage
    print("所有Icon已经下载并位于" + path)

def Migrate():
    print("It works!")
#自动下载当前页面图片和文字
#转换文字至灰机格式
#模拟登录灰机上传至特定页面

# Basic UI
while True:
    ActivateFunction = input("请选择你想要软件执行的功能：按 1 转换特定页面至建筑表格模板格式, 按 2 从特定页面抓取所有图标, 按 3 从Icon页面抓取所有图标")
    if ActivateFunction == '1':
        convertFormat()
    elif ActivateFunction == '2':
        downloadImagesFromPage()
    elif ActivateFunction == '3':
        downloadAllImages()
    else:
        print("输入错误，请重试")