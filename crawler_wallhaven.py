# -*- coding: utf-8 -*-
# @Date     :   2014-12-22
# @Author   :   Lionseun Ling
# @E-mail   :   lionseun@gmail.com 

import os
import urllib.request

def get_html(url):
    """
    Return content of web with url.
    content can write filesystem and it's analysised by webbrowser
    """
    u = urllib.request.URLopener()
#     print(u.addheaders)
    # 清除原本的头部信息
    u.addheaders.clear()
    u.addheader("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0")
    # 使用了后服务器会采用压缩的形式将数据返回到客户端
    # u.addheader("Accept-Encoding", "gzip")
    #可以接受任何类型的数据
    u.addheader("Accept", "*/*")
#     print(u.addheaders)
    tmp = u.open(url)
    content = tmp.read().decode('utf-8')
    tmp.close()
    return content

def analysis_href(html):
    """
    analysis html, and extract url and src lable
    return url tuple
    """
    i = 0
    href = []
    while True:
        try:
            next_href = html[i:].index('href=')+len('href="')
            next_src = html[i:].index('src=')+len('src="')
            if next_href < next_src: 
                i += next_href
            else:
                i += next_src
            tmp_href = html[i: i+html[i:].index('"')]
            if tmp_href.find('alpha.wallhaven.cc') != -1:
                href.append(tmp_href)
            else :
                continue
        except:
            break
    return href

def pic_href(html):
    pic_src = []
    src = analysis_href(html)
    for href in src:
        tmp = href.split(sep = '/')
        if tmp[-1].isdigit() and tmp[-2] == 'wallpaper':
            pic_src.append(href)
        else:
            continue
    return pic_src
        
def get_titile(title, html):
    """
    This is function is only used for alpha.wallhaven.cc
    """
    href = analysis_href(html)
    for url in href:
        if url.find(title) != -1:
            break
    return url

def get_pic_src(url):
    pic_content = get_html(url)
    id = pic_content.index('id="wallpaper"')
    pic_url = pic_content[id : id+pic_content[id:].index('/>')]
    src_num = pic_url.find('src=')+len('src="')
    ret_url = 'http:' + pic_url[src_num : src_num+pic_url[src_num:].find('"')]
    return ret_url

def picture_src(pic_src):
    file_path = './wallpaper'
    download_img = ''
    picture_dir = os.listdir(path = file_path)
    for src in pic_src:
        print('Had download ' + len(picture_dir).__str__() + ' picture')
        # 获取图片的下载地址
        pic_des = get_pic_src(src)
        file_name = pic_des.split(sep='/')[-1]
        if file_name in picture_dir: continue
        # 下载图片
        try:
            download_img = urllib.request.urlretrieve(pic_des, "%s/%s" % (file_path, file_name))
        except:
            continue
        picture_dir.append(file_name)
    return download_img

def html_test(html):
    """
    写入文件，进行解析
    """
    # 找到标题
    title = html[html.index("<title>")+len("<title>"): html.index("</title>")]
#     print(title)
    title = title + ".html"
#     print(title)
    fd = open(title, 'w')
    # 这个函数中操作的文件是属于流
    print(html, file = fd)
    fd.close()

def random_tmp_function():
    url = 'http://alpha.wallhaven.cc'
    content = get_html(url)
    random_url = get_titile('random', html = content)
#     print(random_url)
    random_content = get_html(random_url)
    # 获取html中图片的链接
    href = pic_href(random_content)
    picture_src(href)

def center_print(str):
    length = len(str)
    side = int((80 - length) / 2)
    print(side*'*' + ' ' + str + ' ' + side*'*')

if __name__ == '__main__':
    for i in range(100):
        center_print(str = "The %d random page download start" % (i+1))
        random_tmp_function()
        center_print(str = "The %d random download end" % (i+1))
    while True:
        try:
            random_tmp_function()
        except:
            continue
