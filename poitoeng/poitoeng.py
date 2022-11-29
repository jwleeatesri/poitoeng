# import pandas as pd
import os
from korean_romanizer import Romanizer

from googletrans import Translator; tr = Translator()

# 경로랑 파일. 라이브러리로 올리면 바꾸기
CWD = os.getcwd()
LOAN_WORDS_PATH = os.path.join(CWD,"data","loan_words.csv")
BRANDS_PATH = os.path.join(CWD,"data","brands.csv")
KRDICT_DIR = os.path.join(CWD,"data","krdict")
COMMON_POI_PATH = os.path.join(CWD,"data","common_poi.csv")
USER_DIC_PATH = os.path.join(CWD,"data","user_dic.txt")

from konlpy.tag import Komoran; komoran = Komoran(userdic=USER_DIC_PATH)

def analyze(word:str) -> list:
  """
  word를 형태소로 나눈다. 이때, 사용자 사전(user_dic)에 추가된 브랜드, 흔한 장소 정보, 외래어가 우선시된다.
  Analyzes the `word`. Prioritizes brands, common POIs, loan words added to the `user_dic`.
  """
  word = word.replace(" ","")
  analyzed = []
  cursor = 0
  pos = komoran.pos(word) # 여기서 우선시 되는데 확인해봐야될듯

  for morpheme in pos:
    # ETM = ㄴ 받침
    if morpheme[1] == "ETM":
      count = 0
    else:
      count = len(morpheme[0])
    analyzed.append(word[cursor:(cursor+count)].strip())
    cursor += count
  return [elem for elem in analyzed if elem != ""]

def romanize(morpheme: str)->str:
  """
  형태소를 로마자로 변환.
  Romanizes the morpheme.
  :param str morpheme: morpheme to romanize
  """
  return Romanizer(morpheme).romanize()

def translate_str(morpheme: str)->str:
  """
  형태소를 번역.
  Translates the morpheme.
  :param str morpheme: morpheme to translate
  """
  return tr.translate(morpheme, src="ko").text

def translate_batch(morphemes: list) -> list:
  """
  형태소를 리스트로 한번에 번역.
  Translates a list of morphemes as a batch.
  :param list morphemes: morphemes to translate
  """
  num_morphemes = len(morphemes)
  morphemes = str(morphemes)
  translated = tr.translate(morphemes, src="ko").text[1:-1]
  translated = [t[1:-1] for t in translated.strip().split(', ') if t != ',']
  assert len(translated) == num_morphemes
  return translated

def toeng(poi:str) -> str:
  """
  한글 POI를 영문으로 변환한다.
  Converts Hangul POI data to English.
  :param str poi: hangul poi to translate
  """
  analyzed = analyze(poi)
  converted = ["_"]*len(analyzed)
  for idx, morpheme in enumerate(analyzed):
    if morpheme in loans.keys():
      converted[idx] = loans[morpheme]
    elif morpheme in common_poi.keys():
      converted[idx] = common_poi[morpheme]
    elif morpheme in brands.keys():
      converted[idx] = brands[morpheme]
    else:
      converted[idx] = romanize(morpheme)
  return " ".join(converted).title()
      
def build_dic(fname):
  """
  CSV 파일을 읽고 딕셔너리로 변환한다.
  Converts the csv files to a python dictionary.
  :param str fname: csv file path
  """
  _temp = {}
  with open(fname,"r",encoding="utf-8") as f:
    for row in f.readlines():
      name, nameeng = row.split(",")
      _temp[name.strip()] = nameeng.strip()
  return _temp

if __name__ == "__main__":
  loans = build_dic(LOAN_WORDS_PATH)
  common_poi = build_dic(COMMON_POI_PATH)
  brands = build_dic(BRANDS_PATH)

  print(toeng("할머니고양이삼성아파트"))