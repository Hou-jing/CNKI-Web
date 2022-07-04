#中文识别：官方文档https://cnocr.readthedocs.io/zh/latest/install/
from cnocr import CnOcr

ocr = CnOcr()
res = ocr.ocr('截图.PNG')
print("Predicted Chars:", res)

#英文识别：
import pytesseract
from PIL import Image

image = Image.open('截图.PNG')
code = pytesseract.image_to_string(image, lang='eng')
print(code)
