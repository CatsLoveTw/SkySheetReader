import os
import json
import time


def openFileWithJSON (filePath, mode = "r", encoding = "utf-8"):
    with open(filePath, mode, encoding=encoding, errors="ignore") as f:
        text = f.read()
        f.close()

    try:
        JSON = json.loads(text)[0]
        return JSON
    except json.decoder.JSONDecodeError:
        if encoding == "utf-16":
            return False
        return openFileWithJSON(filePath, mode, encoding="utf-16")


def chosenFile (EXIT):
    _txt = os.listdir("studioTXT")

    txt: list[str] = []
    success = False
    successTXT: list[str] = []

    for i in _txt:
        if i.endswith(".txt"):
            
            f = openFileWithJSON(f"studioTXT/{i}")
            if not f:
                txt.append(i + ".error")# 不符合檔案需求
            else:
                txt.append(i)
                successTXT.append(i)
                success = True


    if success == False:
        if txt.__len__() == 0:
            print("INFO > 請將要讀取的txt檔案放入 studioTXT 資料夾內!")
        else:
            print("ERROR > 檔案內容不符格式而無法使用")
        EXIT()
    else:
        def choose():
            print("CHOOSE > 請輸入指定檔案代號進行解析並產生簡譜 (代號以空格為分隔)")
            print(f"代號: all | 全部txt")
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

            if Select.find("all") != -1:
                selects = []
                for i in range(1, code+1):
                    selects.append(successTXT[i-1])
                
                return selects

            if Select.find(" ") != -1:
                selects: list[str] = []
                for numbers in Select.split(" "):
                    try:
                        selects.append(successTXT[int(numbers)-1])
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
                
                return selects

                
            try:
                selected = successTXT[int(Select)-1]
                return [selected]
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
