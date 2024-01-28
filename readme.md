# SkySheetReader
> 你可以使用該程式，將複雜的「Sky Studio」樂譜轉為簡單易懂的簡譜圖片


## 前置步驟
- 下載 `python` 
- 在該目錄開啟 `CMD`
- 輸入 `pip install -r requirements.txt` 即可下載所需模組 (module)

## 使用說明
- 找到想要的`.txt樂譜`之後確認內容是否為`JSON格式`
- 將樂譜放入 `studioTXT` 資料夾內，並記得檔案名稱
- 在`reader.py`所在目錄打開`CMD`，並輸入`python reader.py`
- 跟著裡面內容輸入即可

## 樂譜獲取
- 若發現該樂譜並非`JSON格式`，請先下載[Sky Studio](#sky-studio載點)
> 詳細的樂譜另存方法可以去網路查詢。
- 載入樂譜後選擇 `另存為` 並選擇 `Json (.txt)` 儲存
- 點入另存樂譜後選擇 `分享` 將檔案匯出
- 找到匯出的檔案後放入 `studioTXT` 資料夾即可

## 主要資料夾介紹
- <`jpg`> 存放所有轉換過後的簡譜
- <`studioTXT`> 將要轉換的Sky Studio樂譜放入此
- <`fonts`> 存放字體的資料夾，刪除將會導致錯誤

## 常見問題
- Q:樂譜放入資料夾後執行程式時找不到檔案 / 提示檔案格式錯誤\
A:樂譜格式不正確，請見[樂譜獲取](#樂譜獲取)

## 作者的話
- 該程式需要使用 `python` 若要在手機上使用的話可以試試 `termux` 喔!

在光遇練琴時，我總喜歡能夠有個「實質上」的樂譜，因此在遇到運用 `Sky Studio` 所製作的樂譜都只能將其捨去，真正能獲得且符合光遇的圖片譜少之又少，而這就是開發此程式的目的，希望各位能夠運用這個程式減少抄譜的負擔，並且將樂譜不再侷限於光遇之中。

## Sky Studio載點
### [IOS](https://apps.apple.com/tw/app/sky-studio/id1522241329)
### [Android](https://play.google.com/store/apps/details?id=com.Maple.SkyStudio)