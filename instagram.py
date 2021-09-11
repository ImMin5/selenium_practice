import time
import random
import re
#import pandas as pd
from datetime import datetime

from apis import get_time
from settings.settings import *
from main import By,WebDriverWait,EC

from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.action_chains import ActionChains


#전역변수
next_arrow_btn_css= "._65Bje.coreSpriteRightPaginationArrow"
heart_btn_css = "._8-yf5"
main_text_object_css="div.C7I1f.X7jCj > div.C4VMK > span"
next_arrow_btn_xpath = "/html/body/div[6]/div[1]/div/div/a[2]"
heart_btn_xpath = '/html/body/div[6]/div[2]/div/article/div[3]/section[1]/span[1]/button/div/span/*[name()="svg"]'
main_text_object_xpath ="/html/body/div[6]/div[2]/div/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span"
insta_id_xpath = "/html/body/div[6]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a"
location_object_xpath ="/html/body/div[6]/div[2]/div/article/header/div[2]/div[2]/div[2]/a"



#LOGIN을 진행하는 함수
def login(driver, username, password) :
	time.sleep(3)
	driver.find_element_by_name('username').send_keys(username)
	time.sleep(1)
	driver.find_element_by_name('password').send_keys(password)
	time.sleep(1)
	driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').submit()
	time.sleep(5)

#인자로 들어오는 해시태그를 COUNT 만큼 게시글을 탐색
#게시물 하나당 2분정도 소요
def click_heart(driver,hash_tag,logger,num):
	startTime = get_time()
	#url 이동
	url = 'https://www.instagram.com/explore/tags/'+hash_tag
	driver.get(url)
	logger.info("\n#################################################################")
	logger.info(str(num) +"번 해시태그 : " + hash_tag)
	logger.info("bot start at "+ startTime)
	logger.info("==========Setting info==========")
	logger.info("LOADING_TIME : "+str(LOADING_TIME)+"s, INTERVAL_HEART : "+str(INTERVAL_HEART)+"s, INTERVAL_NEXT_POST : "+str(INTERVAL_NEXT_POST)+"s")
	logger.info("RANDOMTIME_START : "+str(RANDOMTIME_START)+"s, RANDOMTIME_END : "+str(RANDOMTIME_END)+"s")
	logger.info("COUNT : "+str(COUNT)+"개")
	logger.info("================================")

	WebDriverWait(driver,LOADING_TIME).until(EC.presence_of_element_located((By.XPATH,'//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]/a')))
	driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]/a').send_keys(Keys.ENTER) #최근게시물 첫번째
	#driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a').send_keys(Keys.ENTER) #인기게시물 첫번째


	count = 0
	blockcount = 0
	while count < COUNT :
		randomTime = random.randint(RANDOMTIME_START,RANDOMTIME_END)

		#다음 게시물 버튼 로딩까지 60초 기다림
		try :
			#WebDriverWait(driver, LOADING_TIME).until(EC.presence_of_element_located((By.CSS_SELECTOR, next_arrow_btn_css)))
			#nextBtn=driver.find_element_by_css_selector(next_arrow_btn_css)
			WebDriverWait(driver,LOADING_TIME).until(EC.element_to_be_clickable((By.XPATH,next_arrow_btn_xpath)))
			nextBtn=driver.find_element_by_xpath(next_arrow_btn_xpath)
		except Exception as e:
			logger.info("다음 게시물이 존재하지 않습니다.")
			logger.info(e)
			logger.info("다음 태그로 이동합니다.")
			break

		#좋아요 버튼 로딩까지 60초 기다림
		try :
			WebDriverWait(driver,LOADING_TIME).until(EC.presence_of_element_located((By.XPATH,heart_btn_xpath)))
			heart = driver.find_element_by_xpath(heart_btn_xpath)
			#WebDriverWait(driver, LOADING_TIME).until(EC.presence_of_element_located((By.CSS_SELECTOR, heart_btn_css)))
			#heart=driver.find_element_by_css_selector(heart_btn_css)
		except Exception as e:
			nextBtn.click()
			logger.info("좋아요 로딩 실패! 다음 게시물로 이동")
			logger.info(e)
			continue

		#게시물 내용 읽어오기
		try :
			WebDriverWait(driver,LOADING_TIME).until(EC.presence_of_element_located((By.XPATH,main_text_object_xpath)))
			postContext = driver.find_element_by_xpath(main_text_object_xpath)
			#postContext = driver.find_element_by_css_selector(main_text_object_css)
			postContext = postContext.text
			postContextArray = postContext.split(" ")
			#print(postContext)
		except Exception as e:
			logger.info("Error : 게시물의 내용을 읽기 실패!")
			logger.info(e)
			time.sleep(2)
			nextBtn.click()
			continue

		#게시물에 부적절한 단어가 있는 지 검사
		if add_block(postContextArray,logger) == False :
			blockcount = blockcount + 1
			nextBtn.click()
			time.sleep(1)
			continue


		#좋아요가 눌러져있는지 판단하기 위함
		try :
			heartBtnTxt = driver.find_element_by_xpath(heart_btn_xpath)
			heartBtnTxt = heartBtnTxt.get_attribute('aria-label')
		except Exception as e:
			logger.info('Error : 좋아요 누름 판단 에러')
			logger.info(e)


		#좋아요가 눌러져있으면 그냥 지나침
		try :
			if heartBtnTxt == "좋아요" :
				time.sleep(randomTime)
				heart.click()
				get_id(driver,logger)
				#driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/article/div[3]/section[1]/span[1]/button/div/span/*[name()="svg"]').click()
				#collect_hashtag(postContext,driver)# 좋아요 누른 게시물의 해시태그 수집
				time.sleep(INTERVAL_HEART)
				count = count + 1
		except Exception as e :
			logger.info("Error : 좋아요 클릭 에러")
			logger.info(e)

		try :
			nextBtn.click()
			time.sleep(INTERVAL_NEXT_POST)
		except Exception as e:
			print("다음 게시물로 넘어 갈 수 가 없음...태그 변경")
			logger.info(e)
			print(hash_tag+" 좋아요 완료 게시물 수 "+str(count) +"개 작업완료시간 : "+get_time())
			logger.info("#################################################################\n")
			logger.info(hash_tag+" 좋아요 완료 게시물 수 "+str(count) +"개 작업완료시간 : "+get_time())
			logger.info("#################################################################\n")
			break
	logger.info(hash_tag+"좋아요 완료 게시물 수 "+str(count) +"개 작업완료시간 : "+ get_time())
	logger.info("#################################################################\n")
	return count , blockcount




def add_block(postContext,logger) :
	for i in postContext :
		for j in BLOCK_WORDS :
			if j in i :
				print("차단된 단어 "+j+" in "+i)
				print("다음 게시물로 이동합니다.")
				logger.info("차단된 단어 "+j)
				logger.info("다음게시물로 이동합니다.")
				return False
	return True

def get_id(driver, logger) :
	try :
		id = driver.find_element_by_xpath(insta_id_xpath).text
		logger.info("instagram : "+id)
	except Exception as e :
		print(e)
		logger.info("Error : 인스타그램 아이디 추출 실패")

def get_location(driver, logger) :
	try:
		loaction = driver.find_element_by_xpath(location_object_xpath).text()
		logger.info("location : "+ loaction)
	except Exception as e :
		return





'''
def collect_hashtag(postContext,driver) :
	postDate = driver.find_element_by_xpath('html/body/div[5]/div[2]/div/article/div[3]/div[2]/a/time')
	postDate = postDate.get_attribute('title')
	year = format(datetime.today().year)
	try :
		file = pd.read_csv('./data/'+year+'.xlsx')
		print(postDate)
		tags = re.findall(r'#[^\s#,\\]+', postContext)
		for i in tags :
			print(i)
	except :
		print("엑셀파일 읽기 실패")
		return
'''
