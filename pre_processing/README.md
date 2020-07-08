> # **recipe_preprocess_model.py**
***
 >## 사용된 라이브러리
    import pandas as pd  
    import cx_Oracle  
    import re  

  >## 사용된 메소드

   class RecipePreProcess(): 
    
     def concat_data(self,x,y):       
     def merge_data(self,x,y,on):
         - 두 데이터 프레임을 병합 
     def save_data(self,filename,df):
         - 데이터프레임을 파일로 저장    
     def str_drop_na(self,df):      
	     - 데이터 결측치 행 제거   
	 def df_to_oracle(self.df):
	     -
     def sql_to_clob(self,col,text):  
	     - 데이터 프레임을 오라클에 인서트 
     def select_all_db(self):  
	     -
       
  >## 목적
	  기존 확보한 데이터 에서 결측치를 없애고
	  최종 정리된 데이터를 오라클에 인서트 시키는 작업
	  (python query insert 시간이 오래걸리는 관계로 sqldeveloper에서 데이터 임포트를
	  통해 inset를 수행해도 된다.)
  >## 순서
> 1. catecory, detail 데이터를 recipe_id를 기반으로 merge한다. recipe_raw.csv
> 2. [1]에서 '-'로 치환된 결측치를 제거한다[rec_tag는 삭제한다]. recipe_dropna
> 3. python을 통해 oracle table에 [2]을 insert한다.
> 4. [3]번 작업 불가시 sqldeveloper 데이터 임포트를 사용한다.
> 5. [ 3 or 4 ]후 이상값(insert format error)을 제외하고 테이블을 완성한다.
> 6. [5]테이블을 select하여  recipe_nlp file로 저장한다.

>## 파일
>1. recipe_raw.csv
>2. recipe_dropna.csv
>3. recipe_nlp.csv