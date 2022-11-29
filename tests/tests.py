import unittest
import os
import random

# 로컬
from poitoeng.poitoeng import analyze, toeng, build_dic

CWD = os.getcwd()
LOAN_WORDS_PATH = os.path.join(CWD,"data","loan_words.csv")
BRANDS_PATH = os.path.join(CWD,"data","brands.csv")
KRDICT_DIR = os.path.join(CWD,"data","krdict")
COMMON_POI_PATH = os.path.join(CWD,"data","common_poi.csv")
USER_DIC_PATH = os.path.join(CWD,"data","user_dic.txt")
ALL_DICTS = [LOAN_WORDS_PATH, BRANDS_PATH, COMMON_POI_PATH]

class TestDataModule(unittest.TestCase):
  def test_parse_krdict(self):
    pass

  def test_update_komoran_user_dic(self):
    pass

class TestPoitoengModule(unittest.TestCase):
  def setUp(self):
    loans = build_dic(LOAN_WORDS_PATH)
    common_poi = build_dic(COMMON_POI_PATH)
    brands = build_dic(BRANDS_PATH)

  # 여기서 랜덤으로 데이터 만들고 그거 대상으로 테스팅 ㄱㄱ
  def build_random_test_point(self, num_extract:int)->list:
    """
    테스트용 데이터 생성. 외래어, 브랜드, 흔한 장소 데이터를 임의로 가져와서 조합.
    Generates testing data. Collects loan words, brands, common POI data randomly and combines them.

    :param int num_extract: number of points to extract from each dictionary
    """
    test_data = []
    for dic in ALL_DICTS:
      with open(dic,"r",encoding="utf-8") as f:
        all_data = f.readlines()
        for _ in range(num_extract):
          test_data.append(random.choice(all_data))
    return test_data

  def parse_test_data(self, test_data) -> list:
    """
    테스트용 데이터 파싱. 열을 리스트로 받아서 쉼표 값 기준 나눔. 
    Parse test data. Gets the test data as a list of rows, and separate by commas.
    :param list test_data: test data generated from self.build_random_test_point
    """
    parsed_test_data = []
    for row in test_data:
      _q, _s = row.split(',')
      parsed_test_data.append((_q, _s))
    return parsed_test_data

  # def test_analyze(self):
  #   """
  #   분석 함수가 형태소를 잘 나누는지 확인.
  #   Tests that the script separates the morphemes correctly.
  #   """
  #   test_data = self.build_random_test_point(5)
  #   parsed = self.parse_test_data(test_data)
  #   for _ in range(10):
  #     word_set = random.choices(parsed, k=3)
  #     query = [w[0] for w in word_set]
  #     self.assertEqual(analyze("".join(query)), query) # 한번에 비교해서 퍼센트 낼까
      
  def test_toeng(self):
    test_data = self.build_random_test_point(20)
    parsed = self.parse_test_data(test_data)
    for _ in range(100):
      word_set = random.choices(parsed,k=3)
      query = toeng(" ".join([w[0] for w in word_set]))
      solution = " ".join([w[1] for w in word_set]).title()
      self.assertEqual(query,solution)