import os
import logging
from datetime import datetime

# Logging 설정
logging.basicConfig(filename="data.log", encoding="utf-8",level=logging.DEBUG)

# 여긴 나중에 라이브러리로 올리면 바꾸자
CWD = os.getcwd()
LOAN_WORDS_PATH = os.path.join(CWD,"data","loan_words.csv")
BRANDS_PATH = os.path.join(CWD,"data","brands.csv")
KRDICT_DIR = os.path.join(CWD,"data","krdict")
COMMON_POI_PATH = os.path.join(CWD,"data","common_poi.csv")
USER_DIC_PATH = os.path.join(CWD,"data","user_dic.txt") # 꼭 txt 파일명 유지

# 알파벳(소/대문자) + ' ' + '-'
ALLOWED_CHARACTERS = [chr(i) for i in range(65,91)] + [chr(j) for j in range(97,123)] + [' ','-']

def parse_krdict()->None:
  """
  한국어기초사전(https://krdict.korean.go.kr/)에서 내려받은 자료를 정리하여 외래어와 나머지로 나누어 따로 저장한다.
  사전이 주기적으로 갱신됨으로, 파싱할 때마다 버전 정보와 처리된 날짜를 로그에 기록한다.
  Parses the data downloaded from Korean Basic Dictionary(https://krdict.korean.go.kr/) and separates the data into loan words and others.
  Because the dictionary is updated regularly, we log the version of the dictionary and the date for records keeping.
  """
  with open(LOAN_WORDS_PATH,"r",encoding="utf-8") as f:
    try:
      loan_keys = [line.split(',')[0] for line in f.readlines()]
    except FileNotFoundError:
      loan_keys = []
  with open(LOAN_WORDS_PATH,"a",encoding="utf-8") as loan_words:
    for fname in os.listdir(KRDICT_DIR):
      logging.info(f"{fname} parsed at {datetime.now()}")
      with open(os.path.join(CWD,"data","krdict",fname),"r",encoding="utf-8") as file:
        for row in file.readlines()[1:]: # 첫째줄은 인덱스
          row = row.split(",")
          if (row[4].strip()) != "외래어":
            continue
          if (word := row[0].strip()) not in loan_keys: # 0 = 단어, 4 = 고유어 여부, 5 = 원어
            loan_keys.append(word)
            nameeng = "".join([c for c in row[5].strip() if c in ALLOWED_CHARACTERS])
            loan_words.write(f"{word},{nameeng}\n")

def update_komoran_user_dic()->None:
  """
  한국어기초사전 외래어, 브랜드명, 흔한 장소 정보를 user_dic에 추가한다.
  Adds loan words from the KBD, brand names, common poi to user_dic.
  """
  UPDATE_FROM = [LOAN_WORDS_PATH, BRANDS_PATH, COMMON_POI_PATH]
  with open(USER_DIC_PATH,"r",encoding="utf-8") as userdic:
    userdic_keys = [userdic_item.split(",")[0].strip() for userdic_item in userdic.readlines()]
  with open(USER_DIC_PATH,"a",encoding="utf-8") as userdic_append:
    for dic in UPDATE_FROM:
      with open(dic,"r",encoding="utf-8") as _temp_dic:
        for row in _temp_dic.readlines():
          name = row.split(',')[0]
          if name.strip() not in userdic_keys:
            userdic_append.write(f"{name.strip()}\tNNG\n")
            userdic_keys.append(name.strip())
      logging.info(f"{dic} added to user_dic at {datetime.now()}")

if __name__ == "__main__":
  parse_krdict()
  update_komoran_user_dic()