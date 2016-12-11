from PIL import Image
import subprocess

def cleanImage(filePath, newFilePath):
  image = Image.open(filePath)
  #对图片阈值过滤
  image = image.point(lambda x: 0 if x<143 else 255)
  image.save(newFilePath)
  #OCR识别
  #tesseract可以按自己的要求进行识别训练
  subprocess.call(["tesseract",newFilePath,"output"])
  #获取结果
  outputFile = open("output.txt",'r')
  print(outputFile.read())
  outputFile.close()
  
cleanFile('text_2.jpg','text_2_clean.png')
