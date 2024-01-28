from reportlab.pdfgen import canvas
from reportlab.pdfbase import ttfonts, pdfmetrics
from reportlab.lib.pagesizes import A4
import os
import datetime
import fitz
import math




def setNote(cav: canvas.Canvas, note: list[str], position):
    """
    note 最多7個字/3個元素，若要音符則在字串打一個空格即可
    note 高音符號在數字後面加. 即可 ex:1.
    note 1.. 即為最高音do
    """
    if position["x"] >= 580-92:
        position["x"] = 20
        position["y"] -= 90
    
    if position["y"] <= 60:
        cav.showPage()
        A4_height = A4[1]
        A4_width = A4[0]
        cav.setFillColorRGB(0, 0, 0)
        cav.rect(0, 0, A4_width, A4_height, fill=1)
        position["y"] = 780
        setLine(cav)
        

    colorChanged = False # 是否變化為藍色
    x = position["x"]
    y = position["y"]
    for line in note:
        lineX = x
        for text in line:
            if text != " ":
                if text == "b":
                    colorChanged = True
                    continue
                
                cav.setFont("music", 25)
                if colorChanged == False:
                    cav.setFillColorRGB(1, 1, 1) # 黑色
                else:
                    cav.setFillColorRGB(100/255, 170/255, 250/255) # 藍色
                    colorChanged = False
                cav.drawString(lineX+5, y-21, text)
            lineX += 25 * 0.5 + 2.3
        y -= 20
    
    position["x"] += 110



def setLine(cav: canvas.Canvas):
    x = 20
    for i in range(7):
        y = 780
        for j in range(8):
            # x軸 / 最大 660 最低 20
            # y軸 / 最高 780 最低 60
            # Gray: 128, 128, 128
            cav.setStrokeColorRGB(128/255, 128/255, 128/255)
            cav.line(x, y, x, y-80)
            y -= 90
        x += 110


# 註冊字體
font = ttfonts.TTFont("chinese", "./fonts/NotoSansTC-Light.ttf")
font2 = ttfonts.TTFont("music", "./fonts/SimpMusicBase.ttf")
pdfmetrics.registerFont(font)
pdfmetrics.registerFont(font2)


def createPDF (sheetData: list[str], songName: str):
    # 轉化
    position = {
        "x": 20,
        "y": 780
    }
    def transformText (line: str):
        line = line.replace("1..", "")
        line = line.replace("1..", "")
        line = line.replace("1.", "")
        line = line.replace("2.", "")
        line = line.replace("3.", "")
        line = line.replace("4.", "")
        line = line.replace("5.", "")
        line = line.replace("6.", "")
        line = line.replace("7.", "")
        line = line.replace("1", "")
        line = line.replace("2", "")
        line = line.replace("3", "")
        line = line.replace("4", "")
        line = line.replace("5", "")
        line = line.replace("6", "")
        line = line.replace("7", "")
        line = line.replace("s", "") # 休止
        line = line.replace("p", " ")
        return line


    def charCount (text: str, find: str) -> int:
        if text.find(find) == -1:
            return 0
        else:
            count = 0
            for i in text:
                if i == find:
                    count += 1
            
            return count
        

    # 處理sheetData
    sheetLine1 = transformText(sheetData[0])
    sheetLine2 = transformText(sheetData[1])
    sheetLine3 = transformText(sheetData[2])
    sheetLine4 = transformText(sheetData[3])
    
    
    newLine1 = []
    newLine2 = []
    newLine3 = []
    newLine4 = []



    L1 = math.ceil(sheetLine1.__len__() / 7)
    L2 = math.ceil(sheetLine2.__len__() / 7)
    L3 = math.ceil(sheetLine3.__len__() / 7)
    L4 = math.ceil(sheetLine4.__len__() / 7)
    
    for i in range(L1):
        if sheetLine1 == "":
            break

        text = sheetLine1[0:7]

        counts = charCount(text, "b")
        text = sheetLine1[0:(7+counts)]
        
        newLine1.append(text)
        sheetLine1 = sheetLine1[(7+counts):]
    for i in range(L2):
        if sheetLine2 == "":
            break

        text = sheetLine2[0:7]

        counts = charCount(text, "b")
        text = sheetLine2[0:(7+counts)]
        
        newLine2.append(text)
        sheetLine2 = sheetLine2[(7+counts):]
    for i in range(L3):
        if sheetLine3 == "":
            break

        text = sheetLine3[0:7]

        counts = charCount(text, "b")
        text = sheetLine3[0:(7+counts)]
        
        newLine3.append(text)
        sheetLine3 = sheetLine3[(7+counts):]
    for i in range(L4):
        if sheetLine4 == "":
            break

        text = sheetLine4[0:7]

        counts = charCount(text, "b")
        text = sheetLine4[0:(7+counts)]
        
        newLine4.append(text)
        sheetLine4 = sheetLine4[(7+counts):]



    # pdf
    cav = canvas.Canvas(
        filename="composeDemo.pdf"
    )

    # background
    A4_height = A4[1]
    A4_width = A4[0]
    cav.setFillColorRGB(0, 0, 0)
    cav.rect(0, 0, A4_width, A4_height, fill=1)

    # title
    cav.setFillColorRGB(1, 1, 1)
    cav.setFont("chinese", 36, 1)
    cav.drawCentredString(300, 800, f"~{songName}~")

    # Line
    setLine(cav)


    # Note
    for i in range(newLine1.__len__()):
        setNote(cav, [newLine1[i], newLine2[i], newLine3[i], newLine4[i]], position)
    
    # setNote(cav, ["7123523", "1234567", "12345 7", "1234567"])

    cav.save()


    # PDF & Folder
    if os.path.isdir(f"./jpg/{songName}") == False:
        os.makedirs(f"./jpg/{songName}")

    now = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    os.makedirs(f"./jpg/{songName}/{now}")


    def pdf_image(pdfPath: str, imgPath):
        # 打開PDF
        pdf = fitz.Document(pdfPath)
        # 一頁一頁讀取
        for pg in range(0, pdf.page_count):
            pdf = fitz.Document(pdfPath)
            page = pdf.load_page(pg)
            pm = page.get_pixmap(alpha=False)
            pm._writeIMG(imgPath + str(pg) + ".jpg", format_=1, jpg_quality=100)
            pdf.close()

    pdf_image(r"composeDemo.pdf", f"./jpg/{songName}/{now}/")
