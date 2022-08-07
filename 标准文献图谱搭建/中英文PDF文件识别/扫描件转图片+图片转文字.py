import re
import sys, fitz
import os
import datetime,time

#扫描PDF变为img
def pyMuPDF_fitz(pdfPath, imagePath):
    startTime_pdf2img = datetime.datetime.now()  # 开始时间

    print("imagePath=" + imagePath)
    pdfDoc = fitz.open(pdfPath)
    page_num=pdfDoc.pageCount
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        rotate = int(0)
        # 此处若是不做设置，默认图片大小为：792X612, dpi=72 我扫描的文件是200dpi
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        zoom_x = 1.3  # (1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 1.3
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)

        if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
            os.makedirs(imagePath)  # 若图片文件夹不存在就创建

        pix.writePNG(imagePath + '/' + 'images_%s.png' % (pg + 1))  # 将图片写入指定的文件夹内

    endTime_pdf2img = datetime.datetime.now()  # 结束时间
    print('pdf2img时间=', (endTime_pdf2img - startTime_pdf2img).seconds)
    return page_num


if __name__ == "__main__":
    # pdfPath = 'XXX.pdf'
    pdfPath='E:\\python project\\pythonProject6.27\\标准PDF转化\\扫描件（中）\\GBT 28874-2012 空间科学实验数据产品分级规范.pdf'
    imagePath = 'E:\\python project\\pythonProject6.27\\标准PDF转化\\扫描件图片\\GBT 28874-2012 空间科学实验数据产品分级规范'
    page_num=pyMuPDF_fitz(pdfPath, imagePath)


#图片转为文本
from cnocr import CnOcr
ocr = CnOcr()
dir='E:\\python project\\pythonProject6.27\\标准PDF转化\\扫描件图片\\GBT 28874-2012 空间科学实验数据产品分级规范'


#识别单张图片文本内容
def OCR_singleImg(imgpath):
    res = ocr.ocr(imgpath)
    cont = []
    for each in res:
        if ''.join(each[0]) != '<blank>':
            cont.append(each[0])
    page_text = '\n'.join(cont)
    return page_text
#识别所有图片，整合为标准.txt
def OCR_fileImg(dir):
    time1 = time.time()
    file_list = os.listdir(dir)

    f = open(dir + '\\' + 'easyocr转换文件.txt', mode='w+', encoding='utf_8')
    pages_text={}
    imgnums=0
    for fname in file_list:
        if '.png' in fname:
            imgnums+=1
            pnum = int(re.findall('[0-9]+', fname)[0])
            fpath=dir+'\\'+fname
            page_text=OCR_singleImg(fpath)
            print(page_text)
            pages_text[pnum]=page_text
            print('{}转换完成'.format(fname))
    print('图片总数为{}'.format(imgnums))
    for num in range(1,imgnums+1):
        f.write(pages_text[num])
        f.write('\n')
    time2 = time.time()
    print('标准转换总共耗时%s s' % (time2 - time1))

OCR_fileImg(dir)







