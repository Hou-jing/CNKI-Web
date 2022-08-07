#pdf文件加载为word文件

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.converter import PDFPageAggregator
import os
def parse(pdf_path):
    '''解析PDF文本，并保存到TXT文件中'''
    fp = open(pdf_path, 'rb')
    # 用文件对象创建一个PDF文档分析器
    parser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument(parser)
    # 连接分析器，与文档对象
    parser.set_document(doc)

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDF，资源管理器，来共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释其对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一个page内容
        # doc.get_pages() 获取page列表
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
            # 想要获取文本就获得对象的text属性，
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    with open(pdf_path.replace('.pdf','.txt'), 'a', encoding='utf_8') as f:
                        results = x.get_text()
                        # print(results)
                        f.write(results + "\n")
if __name__ == '__main__':
    dir= '/标准PDF转化/标准文件（中）'
    file_list = os.listdir(dir)
    print('文件总数为{}'.format(len(file_list)))
    for fname in file_list:
        if 'pdf' in fname and 'crd' not in fname and 'doc' not in fname:
            pdf_path = os.path.join(dir,fname)
            parse(pdf_path)
            print('{}文件成功转化为word文件'.format(fname))