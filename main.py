import json
import sys

#셀레니움
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#쓰레딩
from threading import Thread
#크롬드라이버 자동 업데이트
import chromedriver_autoinstaller
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
#시간 함수
import time #sleep 함수 사용
import logging
import os
from instagram import *
from apis import *
from logger import *
from settings.settings import TAGS,LOADING_TIME
from settings.login_info import PASSWORD
USERNAME = "_dhtex"

def main():
	totalHeartCount = 0
	totalBlockedCount = 0
	options = webdriver.ChromeOptions() #크롬 옵션 설정
	options.add_argument('--disable-gpu')
	options.add_argument('--incognito')
	options.add_argument("window-size=1200x600")
	#options.add_argument('--disable-logging')
	#options.add_argument('headless') #창없애기
	#options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/14.0.3")
	#options.add_argument("no-sandbox")

	chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인
	chromedriver = chrome_ver+'/chromedriver'
	chromedriver = resource_path(chromedriver)

	if os.path.isfile(chromedriver) :
		driver = webdriver.Chrome(chromedriver, options=options)
	else :
		chromedriver_autoinstaller.install(True)
		driver = webdriver.Chrome(chromedriver, options=options)

	driver.get('https://www.instagram.com/accounts/login/')


	try :
		startTime = time.time()
		startTime2 = get_time()
		WebDriverWait(driver,LOADING_TIME).until(EC.presence_of_element_located((By.NAME,'username')))
		login(driver, USERNAME,PASSWORD)

		directory = create_folder(resource_path('data/'+get_date_dir()))
		log_file = create_file(get_day()+'.txt',directory)
		logger = create_logger(log_file)

		#directory = create_folder(resource_path('data/error'))
		#log_error_file = create_file('error.txt',directory)
		#logger_error = create_logger_error(log_error_file)


		logger.info("LOGIN START!")
		logger.info("instagram : "+USERNAME)

		#태그 랜덤배열
		RTAGS = make_rand_array(TAGS)
		hash_tags = ""
		num = 1
		for i in RTAGS :
			x , y = click_heart(driver, i,logger,num)
			totalHeartCount = totalHeartCount + x
			totalBlockedCount = totalBlockedCount + y
			num = num +1
			hash_tags = hash_tags + i + ", "
	except Exception as e :
		print("main()에러 : ",e)		
	finally :

		endTime = time.time()
		if totalHeartCount == 0 :
			logger.info("좋아요 누른 게시물 : " + str(totalHeartCount)+" 개")
		else :
			logger.info("해시태그 목록 : " + hash_tags)
			logger.info("좋아요 누른 게시물 : " + str(totalHeartCount)+" 개")
			logger.info("차단된 광고 게시물 : "+ str(totalBlockedCount)+" 개")
			logger.info("시작 시간 : "+ startTime2)
			logger.info("종료 시간 : "+get_time())
			totalTime = endTime - startTime
			logger.info("총 소요시간 : "+str(round(totalTime/60,2))+" 분")
			logger.info("태그별 평균 소요시간 : "+str(round(totalTime/60/len(TAGS),2))+" 분")
			logger.info("게시글 평균 소요시간 : "+str(round(totalTime/totalHeartCount,2))+" 초	")
			driver.quit()

def start_menu() :
	print("프로그램 종료 : 0")
	print("프로그램 시작 : 1")


if __name__ == "__main__":
	flag_main = False
	CMD = 1
	main()

