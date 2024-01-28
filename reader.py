print("INFO > 正在載入資源套件")
import json
from Maker import createPDF
import time
import os
import init
import Chooser

# ~~~Setting~~~
needKey2 = True # 是否讀取"藍色按鈕"


def EXIT ():
    print("EXIT > 程式將在 10 秒後退出")
    time.sleep(10)
    exit(0)



file = Chooser.chosenFile(EXIT)
print("~~~~~~~~~生成中~~~~~~~~~")
with open(f"studioTXT/{file}", "r", encoding="utf-8") as f:
    text = f.read()
    f.close()

Compose = json.loads(text)[0]

songName = Compose["name"]

notes = Compose["songNotes"]

newNotes = []
for note in notes:
    noteTimes = note["time"]
    key = note["key"]
    if needKey2 == False:
        if key.split("Key")[0] == "2":
            continue


    if newNotes.__len__() != 0:
        try:
            try:
                note2 = newNotes[newNotes.__len__()-1]
                deleteCount = 1
                beforeNote = note2[note2.__len__()-deleteCount]
                beforeTimes = beforeNote["time"]
                beforeKey = beforeNote["key"].split("Key")[1]
            except IndexError:
                pass
        except TypeError:
            note2 = newNotes[newNotes.__len__()-1]
            deleteCount = 2
            beforeNote = note2[note2.__len__()-deleteCount]
            beforeTimes = beforeNote["time"]
            beforeKey = beforeNote["key"].split("Key")[1]


        if noteTimes == beforeTimes:
            if beforeKey == key.split("Key")[1]:
                note2[note2.__len__()-deleteCount] = note
                note2.pop()
                continue

            newNotes[newNotes.__len__()-1].append(note)
            if key.split("Key")[0] == "2":
                newNotes[newNotes.__len__()-1].append("b")
        else:
            minus = noteTimes - beforeTimes
            while minus >= 300:
                newNotes.append(["p"])
                minus -= 300
            if key.split("Key")[0] == "2":
                newNotes.append([note, "b"])
            else:
                newNotes.append([note])
    else:
        if key.split("Key")[0] == "2":
            newNotes.append([note, "b"])
        else:
            newNotes.append([note])

sheets = [
    "", # 主旋律
    "", # 和弦1
    "", # 和弦2
    ""  # 和弦3
]



for notes in newNotes:
    bCounts = 0 # 紀錄顏色數量
    coloredNotes: list[str] = []
    nowSheetsIndex = 0
    continueIndex = -1 # 處理顏色音
    for i in range(notes.__len__()):
        nowSheetsIndex = i-bCounts
        if (i - bCounts) == 4:
            break # 太多和弦 暫時不支援

        if notes[notes.__len__()-1-i] == "p": # 間隔
            for k in range(sheets.__len__()):
                sheets[k] += "p"
            continue

        if (i+1) == notes.__len__():
            if (notes.__len__() - int(bCounts / 2)) < 4:
                for j in range(int(i+1-bCounts / 2), 4):
                    sheets[j] += "p"

        if i == continueIndex:
            continue

        
        
        
        if notes[notes.__len__()-1-i] == "b": # 藍色
            key = int(notes[notes.__len__()-i-2]["key"].split("Key")[1])
            key += 1
            
            if key == 15:
                key = "1.."
            elif key >= 8:
                key = f"{key-7}."
            else:
                key = key.__str__()

            coloredNotes.append("b" + key)
            bCounts += 2
            continueIndex = i+1
            continue
        
        key = int(notes[notes.__len__()-1-i]["key"].split("Key")[1])
        key += 1

        if key == 15:
            key = "1.."
        elif key >= 8:
            key = f"{key-7}."
        else:
            key = key.__str__()
        
        sheets[i-bCounts] += key
        
    
    for coloredNote in coloredNotes:
        nowSheetsIndex += 1 # 要填入的Index

        sheets[nowSheetsIndex] += coloredNote
        

createPDF(sheets, songName)

os.remove("composeDemo.pdf")
print("SUCCESS > 簡譜製造成功，去 jpg 資料夾看看吧!")
EXIT()