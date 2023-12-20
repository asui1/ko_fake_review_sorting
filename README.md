# ko_fake_review_sorting
graduation research to find fake reviews of restaurants on a map.

You can see all datas in all_data.xlsx label 0 or 1 : real review, label 2 : gpt-generated fake review.

# This is Steps of Researches and Their files.
- Due to copyrights and size limits, some data are missing so take this code only as a reference.

1. Review Data crawling from naver map. (dataCrawling.py, collected_reviews)

2. preprocess text(data_refine.py)

3. get fake reveiw data (NYC_restaurant review dataset was used, get_yelp_fake.py)

4. train chat gpt with english fake reviews and generate fake reviews (gpt_review_finetuning.py, chatgpt_training.py, yelp_gpt_data)

5. translate english reviews to korean reviews (yelp_gpt_kor_data)

6. use korean gpt models to calculate text similarity (distance.py)

7. Do K-medoids clustering (augsts_kmedoids.py)

8. sentiment analysis of review text (sentiment.py)

9. report and result (pdf files)

----------------------------------------------------

# 연구 단계와 관련 파일입니다.
- 혹시 모를 저작권 및 크기 제한으로 인해 일부 데이터가 누락되었으므로 이 코드는 참고용으로만 사용하세요.

1. 네이버 지도에서 데이터 크롤링을 수행합니다. (dataCrawling.py, collected_reviews)

2. 텍스트 전처리(data_refine.py)

3. 가짜 리뷰 데이터 가져오기(NYC_restaurant 리뷰 데이터셋 사용, get_yelp_fake.py)

4. 영어 가짜 리뷰로 chat gpt를 훈련시키고 가짜 리뷰 생성(gpt_review_finetuning.py, chatgpt_training.py, yelp_gpt_data)

5. 영어 리뷰를 한국어 리뷰로 번역 (YELP_GPT_KOR_DATA)

6. 한국어 GPT 모델을 사용하여 텍스트 유사도 계산 (distance.py)

7. K-Medoids 클러스터링 수행(augsts_kmedoids.py)

8. 리뷰 텍스트의 감성 분석 (sentiment.py)

9. 보고서 및 결과(PDF 파일들)