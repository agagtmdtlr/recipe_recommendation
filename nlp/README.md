## Info_nlp_03.py
>### 사용 라이브러리 

    from konlpy.tag import Okt,Mecab  
    import pandas as pd  
    import re,time
	from multiprocessing import Pool
	
>### 사용 매소드

    class Source:  
       def __init__(self):  
    	   -  식재료 표준화를 위한 정리 자료 호출
       def subset_kwd(self,row):  
	       -  통일 되지 않은 식재료들 표준화 처리
          
   
 >### 목적
	  너무 다양한 식재료를 데이터로 활용 하기 위해서
	  표준화 처리를 진행 