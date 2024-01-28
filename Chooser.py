import os
import json
import time


def chosenFile (EXIT):
    _txt = os.listdir("studioTXT")

    txt: list[str] = []
    success = False
    successTXT: list[str] = []

    for i in _txt:
        if i.endswith(".txt"):
            with open(f"studioTXT/{i}", "r", encoding="utf-8") as f:
                text = f.read()
                f.close()
            try:
                json.loads(text)[0]
                txt.append(i)
                successTXT.append(i)
                success = True
            except json.decoder.JSONDecodeError:
                txt.append(i + ".error")# 不符合檔案需求


    if success == False:
        if txt.__len__() == 0:
            print("INFO > 請將要讀取的txt檔案放入 studioTXT 資料夾內!")
        else:
            print("ERROR > 檔案內容不符格式而無法使用")
        EXIT()
    else:
        def choose():
            print("CHOOSE > 請輸入指定檔案代號進行解析並產生簡譜")
            code = 0
            for i in range(txt.__len__()):
                if txt[i].endswith(".error"):
                    print(f"代號: | {txt[i].replace('.error', '')} | 該檔案因內容不符格式而無法使用")
                else:
                    code += 1
                    print(f"代號:{code} | {txt[i]}")

            Select = input("輸入代號 (若要退出則打exit即可)")

            if Select == "exit":
                exit(0)
                
            try:
                selected = successTXT[int(Select)-1]
                return selected
            except ValueError:
                print("ERROR > 輸入內容不正確，3秒後重試")
                time.sleep(3)
                print("~~~~~~~~~TRY AGAIN~~~~~~~~~")
                choose()
            except IndexError:
                print("ERROR > 找不到指定代號的檔案，3秒後重試")
                time.sleep(3)
                print("~~~~~~~~~TRY AGAIN~~~~~~~~~")
                choose()
        return choose()
