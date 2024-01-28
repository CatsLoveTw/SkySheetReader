import os

if os.path.isdir(f"./jpg") == False:
    os.makedirs("./jpg")

if os.path.isdir(f"./studioTXT") == False:
    os.makedirs("./studioTXT")