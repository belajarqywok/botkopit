#!/bin/env python3
#!/bin/env python3
import os
import sys
# import csv
import json
import numpy
import pymysql
import datetime
import requests
from gtts import gTTS
import pandas as pd
from time import sleep
from pydub import AudioSegment
from pydub.playback import play
# from bs4 import BeautifulSoup 
# import mysql.connector as mysqlConnect
# tes koneksi
# menguji kalau koneksi stabil,tidak stabil, koneksi bermasalah
respon=os.system("ping -c 1 " + "google.com")
if respon == 0:
    os.system("clear")
else:
    os.system("clear")
    print('\033[31;1m'+"[ ! ] koneksi anda bermasalah..."+'\033[37;1m')
    sys.exit(1)
#mengambil data
dataKorona=requests.get("https://services5.arcgis.com/VS6HdKS0VfIhv8Ct/arcgis/rest/services/COVID19_Indonesia_per_Provinsi/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json")
korona=json.loads(dataKorona.content)
#klasifikasi dan pengurutan data
namaProvinsi = []
positif = []
sembuh = []
meninggal = []
#pengurutan data
for urutanProvinsi in range(len(korona['features'])-1):
    namaProvinsi.append(korona["features"][urutanProvinsi]["attributes"]["Provinsi"])
    positif.append(korona["features"][urutanProvinsi]["attributes"]["Kasus_Posi"])
    meninggal.append(korona["features"][urutanProvinsi]["attributes"]["Kasus_Meni"])
    sembuh.append(korona["features"][urutanProvinsi]["attributes"]["Kasus_Semb"])
sort=[]
for length in range(len(korona['features'])-1):
    sort.append({
        "nama provinsi":namaProvinsi[length],
        "positif":positif[length],
        "meninggal":meninggal[length],
        "sembuh":sembuh[length]
    })
setTime=input("[ ? ] masukan waktu pengambilan data > ")
while True:
    if datetime.datetime.now().strftime("%X")==setTime:
        try:
            #record ke csv
            def rec_CSV(namaFile):
                df=pd.DataFrame(sort)
                df.to_csv("csv/"+namaFile+".csv", index=False, encoding="utf-8")
            rec_CSV(datetime.datetime.now().strftime("%Y%m%d%H"))
            #tanda
            print("[ + ] data diambil....... ")
            music = AudioSegment.from_mp3("cencor.mp3")
            play(music)
            sleep(1)
            os.system("clear")
            #orang ngomong
            def orang_ngomong(jumlah):
                arrNgomong=[]
                for ngomomg in range(jumlah):
                    arrNgomong.append("provinsi "+namaProvinsi[ngomomg]+". positif "+str(positif[ngomomg])+" orang. meninggal "+str(meninggal[ngomomg])+" orang."+" sembuh "+str(sembuh[ngomomg])+" orang")
                tulisan=arrNgomong[0]
                for index in range(jumlah-1):
                    tulisan=tulisan+"."+arrNgomong[index+1]
                eksekusi = gTTS(text=tulisan, lang='id', slow=False)
                eksekusi.save("ngomong.mp3")
                suara = AudioSegment.from_mp3("ngomong.mp3")
                play(suara) 
            orang_ngomong(len(korona['features'])-1)
        except KeyboardInterrupt:
            os.system("clear")
            print("keluar program.....")
            sys.exit(1)
    else:
        try:
            print("[ + ] data diproses ")
            sleep(1)
            os.system("clear")
        except KeyboardInterrupt:
            os.system("clear")
            print("keluar program.....")
            sys.exit(1)
            
