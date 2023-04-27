from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.keys import Keys
import time
import os
from flask import Flask, Response, render_template, request, jsonify
from datetime import timedelta, date
import tabula
import PyPDF2
import fitz
import pandas as pd




def delete_files():
    os.system('del "C:\\Users\\admin\\Desktop\\project mainpdfs\\pdfs\\*.pdf"')


app = Flask(_name_)


opt=Options()
opt.add_argument("start-maximized")
opt.add_argument("--disable-notifications")
opt.add_argument("--no-sandbox")
opt.add_argument("--disable-popup-window")
opt.add_argument("--disable-extensions")
opt.add_experimental_option("prefs", { \
'download.default_directory' : 'C:\\Users\\admin\\Desktop\\project mainpdfs\\pdfs',
"profile.default_content_setting_values.media_stream_mic": 0,
"profile.default_content_setting_values.media_stream_camera":0,
"profile.default_content_setting_values.geolocation": 0,
"profile.default_content_setting_values.notifications": 0,
"credentials_enable_service": False,
"profile.password_manager_enabled": False
})




def download_wait(path_to_downloads):
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < 20:
        time.sleep(1)
        dl_wait = False
        for fname in os.listdir(path_to_downloads):
            if fname.endswith('.crdownload'):
                dl_wait = True
        seconds += 1
    return seconds


def loadfile(dates__):
    driver=webdriver.Chrome(chrome_options=opt, executable_path='chromedriver.exe')
    driver.get('https://wrd.guj.nic.in/dam/')
    wait = WebDriverWait(driver, 10)
    time.sleep(1)
    driver.find_element("xpath","/html/body/div[1]/div/div[6]/div/div/div[3]/button").click()
    for date__ in dates__:
        time.sleep(0.5)
        driver.find_element("xpath","/html/body/div/div/div[5]/div[1]/div[1]/div[2]/label/input").clear()
        driver.find_element("xpath","/html/body/div/div/div[5]/div[1]/div[1]/div[2]/label/input").send_keys(date__)
        time.sleep(0.5)
        driver.find_element("xpath","/html/body/div/div/div[5]/div[1]/div[1]/table/tbody/tr/td[2]/a").click()
    while True:
        download_wait('C:\\Users\\admin\\Desktop\\project mainpdfs\\pdfs')
        break
    driver.quit()

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta


def convert_into_csv(date___s):
    pdf_loc = 'C:\\Users\\admin\\Desktop\\project mainpdfs\\pdfs'
    csv_loc = 'C:\\Users\\admin\\Desktop\\project mainpdfs\\pdfs'
    all_file_lst = os.listdir(pdf_loc)

    lst_of_all_df = []
    
    print(all_file_lst)
    for x in all_file_lst:
        full_name = pdf_loc+"\\"+x
        new_full_name = pdf_loc+"\\1"+x
        
        reader = PyPDF2.PdfFileReader(full_name)
        start_pg = -1
        end_pg = -1
        result_list = []
        for page_number in range(0, reader.numPages):
            page = reader.getPage(page_number)
            page_content = page.extractText()
            
            if page_content.find('Gross Storage of major schemes')!=-1:
                start_pg=page_number

            if page_content.find('STATEMENT SHOWING PERCENTAGE STORAGE')!=-1:
                end_pg=page_number

        print(str(start_pg)+'-'+str(end_pg))
        print('\n')

        ipf = full_name
        opf = new_full_name
        f = fitz.open(ipf)
        pags = []
        for y in range(start_pg+1,end_pg):
            pags.append
        print(pags)
        pgls = pags
        f.select(pgls)
        f.save(opf)



        df = tabula.read_pdf( new_full_name ,encoding='utf-8',stream=True,pages='all')[0]
        lst_of_all_df.append(df)
        # print(df.values.tolist())
        # tabula.convert_into(new_full_name, csv_loc+"\\"+x.split('.')[0]+'.csv' , output_format="csv", pages='all')
    excl_merged = pd.DataFrame()
    for excl_file in lst_of_all_df:
        excl_merged = excl_merged.append(excl_file, ignore_index=True)
    name_of_csv = "".join(date__s)
    excl_merged.to_excel(name_of_csv+'.xlsx', index=False)




@app.route("/",methods=["GET","POST"])
def get_date():
    json_data = {}
    delete_files()
    sdate1=request.args.get('sdate')
    edate1=request.args.get('edate')
    sdate = date( int(sdate1.split('-')[-1]) , int(sdate1.split('-')[1]) , int(sdate1.split('-')[0]) )
    edate = date( int(edate1.split('-')[-1]) , int(edate1.split('-')[1]) , int(edate1.split('-')[0]) )

    all_dates=[]
    for x in daterange(sdate, edate):
        all_dates.append( x.strftime('%d-%m-%Y') )
    print('\n\n\n',all_dates,'\n\n\n')
    loadfile(all_dates)
    convert_into_csv(all_dates)

    return jsonify(json_data)


app.run(debug = True, threaded=True, host='0.0.0.0', port=5000)
