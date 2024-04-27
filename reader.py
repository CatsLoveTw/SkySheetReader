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



files = Chooser.chosenFile(EXIT)
count = 0

for file in files:
    count += 1
    print(f"\r~~~~~~~~~生成中 ({count}/{files.__len__()})~~~~~~~~~", end="")

    Compose = Chooser.openFileWithJSON(f"studioTXT/{file}")

    songName = Compose["name"]

    songSpeed = Compose["bpm"]

    try:
        songAuthor = Compose["author"]
    except KeyError:
        # 好像有些舊版不會有Author和transcribedBy
        songAuthor = "None"

    try:
        transcribedBy = Compose["transcribedBy"]
    except KeyError:
        transcribedBy = "None"

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
                    # note2.pop()
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
        "",  # 和弦3
        "",  # 和弦4
        "",  # 和弦5
    ]



    for notes in newNotes:
        bCounts = 0 # 紀錄顏色數量
        coloredNotes: list[str] = []
        nowSheetsIndex = 0
        continueIndex = -1 # 處理顏色音
        for i in range(notes.__len__()):
            nowSheetsIndex = i-bCounts
            if (i - bCounts) == sheets.__len__():
                break # 太多和弦 暫時不支援

            if notes[notes.__len__()-1-i] == "p": # 間隔
                for k in range(sheets.__len__()):
                    sheets[k] += "p"
                continue

            if (i+1) == notes.__len__():
                if (notes.__len__() - int(bCounts / 2)) < sheets.__len__():
                    for j in range(int(i+1-bCounts / 2), sheets.__len__()):
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
            

    # print(sheets)
    noteRange = 0
    for i in sheets:
        if i.replace("p", "").__len__() > 0:
            noteRange += 1


    createPDF(sheets, songName, noteRange, songSpeed, songAuthor, transcribedBy)

    try:
        os.remove("composeDemo.pdf")
    except: 
        pass

print("\nSUCCESS > 簡譜製造成功，去 jpg 資料夾看看吧!")
EXIT()