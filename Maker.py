from reportlab.pdfgen import canvas
from reportlab.pdfbase import ttfonts, pdfmetrics
from reportlab.lib.pagesizes import A4
import os
import datetime
import fitz
import math




def setNote(cav: canvas.Canvas, note: list[str], position, noteRange: int):
    """
    note 最多7個字/3個元素，若要音符則在字串打一個空格即可
    note 高音符號在數字後面加. 即可 ex:1.
    note 1.. 即為最高音do
    """
    if position["x"] >= 580-92:
        position["x"] = 20
        position["y"] -= noteRange * 16 + 30
        
    
    if position["y"] <= noteRange * 16 + 30:
        cav.showPage()
        A4_height = A4[1]
        A4_width = A4[0]
        cav.setFillColorRGB(0, 0, 0)
        cav.rect(0, 0, A4_width, A4_height, fill=1)
        position["y"] = 780
        setLine(cav, noteRange)
        

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



def setLine(cav: canvas.Canvas, noteRange: int):
    x = 20
    for i in range(7):
        y = 780
        for j in range(18):
            # x軸 / 最大 660 最低 20
            # y軸 / 最高 780 最低 60
            # Gray: 128, 128, 128
            if y <= noteRange * 16 + 30:
                break
            cav.setStrokeColorRGB(128/255, 128/255, 128/255)
            cav.line(x, y, x, y-(noteRange * 16 + 20))
            y -= noteRange * 16 + 30
        x += 110


# 註冊字體
font = ttfonts.TTFont("chinese", "./fonts/NotoSansTC-Light.ttf")
font2 = ttfonts.TTFont("music", "./fonts/SimpMusicBase.ttf")
pdfmetrics.registerFont(font)
pdfmetrics.registerFont(font2)


def createPDF (sheetData: list[str], songName: str, noteRange: int, songSpeed: int, author: str, transcibed: str):
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
    
    Lines_End = []
    Lines_First = []
    for sheet in sheetData:
        newLine = []

        sheetLine = transformText(sheet)
        LineLength = math.ceil(sheetLine.__len__() / 7)
        # print("a", charCount(sheetLine, "b"))
        # print(LineLength)
        bCount = 0
        for i in range(LineLength):
            if sheetLine == "":
                # print("test", i)
                break

            text = sheetLine[0:7]
            
            counts = charCount(text, "b")
            
            text = sheetLine[0:(7+counts)]
            while True:
                if (text.replace("b", "").__len__() < 7) and text.__len__() != sheetLine.__len__():
                    counts += 1
                    text = sheetLine[0:(7+counts)]
                else:
                    break
            bCount += counts
            # text = sheetLine[0:(7+counts)]
            
            newLine.append(text)
            sheetLine = sheetLine[(7+counts):]
        # print("b", bCount)
        
        Lines_First.append(newLine)
    
    # print(Lines_First)
    
    for i in range(Lines_First[0].__len__()):
        L2 = []
        for j in range(Lines_First.__len__()):
            # print(Lines_First.__len__(), Lines_First[j].__len__())
            L2.append(Lines_First[j][i])
        
        Lines_End.append(L2)

    # print(Lines_End)
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

    # author & speed & transcribed
    cav.setFillColorRGB(1, 1, 1)
    cav.setFont("chinese", 13, 1)
    cav.drawString(450, 815, f"作者: {author}")

    cav.setFillColorRGB(1, 1, 1)
    cav.setFont("chinese", 13, 1)
    cav.drawString(450, 800, f"改編: {transcibed}")

    cav.setFillColorRGB(1, 1, 1)
    cav.setFont("chinese", 13, 1)
    cav.drawString(15, 800, f"曲速: {songSpeed}")


    # Line
    setLine(cav, noteRange)


    # Note
    for newLine1 in Lines_End:
        # print(newLine1)
        setNote(cav, newLine1, position, noteRange)
    
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
