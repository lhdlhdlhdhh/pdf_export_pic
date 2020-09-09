import fitz
import time
import re
import os


def pdf2pic(path, pic_path):
    # t0 = time.clock()                          # 生成图片初始时间
    checkXO = r"/Type(?= */XObject)"           # 使用正则表达式来查找图片
    checkIM = r"/Subtype(?= */Image)"
    doc = fitz.open(path)                      # 打开pdf文件
    imgcount = 0                               # 图片计数
    lenXREF = doc._getXrefLength()             # 获取对象数量长度
     
    # 打印PDF的信息
    print("文件名:{}, 页数: {}, 对象: {}".format(path, len(doc), lenXREF - 1))
     
    # 遍历每一个对象
    for i in range(1, lenXREF):
        text = doc._getXrefString(i)            # 定义对象字符串
        isXObject = re.search(checkXO, text)    # 使用正则表达式查看是否是对象
        isImage = re.search(checkIM, text)      # 使用正则表达式查看是否是图片
        if not isXObject or not isImage:        # 如果不是对象也不是图片，则continue
            continue
        imgcount += 1
        pix = fitz.Pixmap(doc, i)               # 生成图像对象
        new_name = "图片{}.png".format(imgcount) # 生成图片的名称
        if pix.n < 5:                           # 如果pix.n<5,可以直接存为PNG
            pix.writePNG(os.path.join(pic_path, new_name))
        else:                                   # 否则先转换CMYK
            pix0 = fitz.Pixmap(fitz.csRGB, pix)
            pix0.writePNG(os.path.join(pic_path, new_name))
            pix0 = None
        pix = None                              # 释放资源
        # t1 = time.clock()                       # 图片完成时间
        # print("运行时间:{}s".format(t1 - t0))
        print("提取了{}张图片".format(imgcount))
         
if __name__=='__main__':
    m_list = [
        'meipian-B18311751-books-inner-1-1',
        'meipian-B18316618-books-inner-2-1',
        'meipian-B18345273-books-inner-3-1',
        'meipian-B18346782-books-inner-1-1',
        'meipian-B18374698-books-inner-1-1',
        'meipian-B18375578-books-inner-1-1',
        'meipian-B18410920-books-inner-1-1',
        'meipian-B18422324-books-inner-3-3',
        'meipian-B18438130-books-inner-1-1',
        'meipian-B18451790-books-inner-1-1',
    ]
    for m in m_list:
        path = r"/home/d/Desktop/work/server-master/pdfs/%s.pdf" % m
        pic_path = r'/home/d/Desktop/work/server-master/pdfs/pic/%s' % m.split('-')[1]
        # 创建保存图片的文件夹
        if os.path.exists(pic_path):
            print("文件夹已存在，不必重新创建！")
            pass
        else:
            os.mkdir(pic_path)
        pdf2pic(path, pic_path)
