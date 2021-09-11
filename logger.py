import logging
import os
import datetime

def create_logger_error(directory) :
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)
    # log 출력 형식
    formatter = logging.Formatter('[ERROR] : %(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # log를 파일에 출력
    file_handler = logging.FileHandler(directory)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def create_logger_warn(directory) :
    logger = logging.getLogger()
    logger.setLevel(logging.WARING)
    # log 출력 형식
    formatter = logging.Formatter('[WARN] : %(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # log를 파일에 출력
    file_handler = logging.FileHandler(directory)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def create_logger(directory) :


    '''
    logger= logging.getLogger(directory)
    # Check handler exists
    if len(logger.handlers) > 0:
        logger.handlers.clear()
    '''
    logger = logging.getLogger()
    # 로그의 출력 기준 설정
    logger.setLevel(logging.INFO)

    # log 출력 형식
    formatter = logging.Formatter('[INFO] : %(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # log 출력
    #stream_handler = logging.StreamHandler()
    #stream_handler.setFormatter(formatter)
    #logger.addHandler(stream_handler)


    # log를 파일에 출력
    file_handler = logging.FileHandler(directory)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger