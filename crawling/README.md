


> # **nlp_crawling_model.py**
 ## 사용된 메소드

    class_Crawl()
         - Crawl_category_id()
	         # 대분류별 중분류 정보 수집
         - Crawl_recipe_id()
		     # 중분류별 레시피 id 수집
         - Crawl_recipe_id_by_category4()
	         # 추가정보를 통한 중분류 리스트 수집
         - Crawl_recipe_detail()
		     # 각id를 통한 각컬럼 기초 데이터 수집

## 목적

해당 홈페이지에서 크롤링을 통하여 모든 레시피를 추출하여 이후 작업에 필요로 하는 데이터형태로 1차 가공

> ## 순서
> 1. url request parameter에 사용할 category id를 가져와 instance 변수에 저장.
> 2. [1]instance 변수를 불러와 category id를 기반으로 검색하여 recipe_id를 가져온다. (use 1 ~ 3 category)
> 3. [1]instance 변수를 불러와 category 4 id를 기반으로 검색하여 recipe_id 가져온다.
> 4. [2],[3] 데이터를 recipe_id를 기반으로 merge 한다. (category id는 value로 치환한다.)
> 5. recipe_id를 사용하여 레시피별 상세 페이지로 들어가 title,sub,source,step를 추출(없으면 '-' 치환)해서 저장한다.
