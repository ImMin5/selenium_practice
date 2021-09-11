import random
import datetime
import os

#생대경로 구하는 함수
def resource_path(relative_path):
	try:
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")

	return os.path.join(base_path, relative_path)

#해쉬태그를 랜덤으로 섞어주는 함수
def make_rand_array(arrays) :
	try :
		_len = len(arrays)
		used = [False for i in range(0,_len)] 
		randTags = [0 for i in range(0,_len)]
		count = 0

		while count < _len :
			rnum = random.randint(0,_len-1)
			if used[rnum] == False :
				randTags[count] = arrays[rnum]
				used[rnum] = True
				count = count + 1
	except Exception as e:
		print("apis -> make_rand_array() 에러 발생")
		print('에러 내용 : ',e) 
	finally :
		return randTags

#시간 구하는 함수
def get_time() :
	now = datetime.datetime.now()
	nowDate = now.strftime('%Y-%m-%d')
	nowTime = now.strftime('%H:%M:%S')
	nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
	return nowDatetime

def get_day() :
	now = datetime.datetime.now()
	nowDay = now.strftime('%d')
	return nowDay


#로그 저장폴더를 만들기 위한 날짜 return
def get_date_dir() :
	now = datetime.datetime.now()
	nowDate = now.strftime('%Y/%m')
	return nowDate


#폴더 만들기
def create_folder(directory) :
	try :
		if not os.path.exists(directory) :
			os.makedirs(directory)
		return directory
	except OSError :
		print('Error : Creating directory. ' + directory)

#파일 만들기
def create_file(filename,dir) :
	path = dir+'/'+filename
	try :
		file = open(path,'a+')
		#file.close
		return path
	except :
		print("Can't make file : " + path)
