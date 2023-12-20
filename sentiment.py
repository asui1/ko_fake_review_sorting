from sentence_transformers import SentenceTransformer, util
from openpyxl import load_workbook
from openpyxl import Workbook
import torch
import numpy
from transformers import AutoModel, AutoTokenizer
from transformers import pipeline
import torch
import sys
import requests
import json
import time
#신뢰도 99%, 오류 +-3%일때 1675개의 샘플을 확보해야함.
#stratified random sampling 방법으로 proportional하게 값을 추출함.


client_id = ""
client_secret = ""
url="https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"
headers = {
    "X-NCP-APIGW-API-KEY-ID": client_id,
    "X-NCP-APIGW-API-KEY": client_secret,
    "Content-Type": "application/json"
}

workbook = load_workbook("self_made_review.xlsx")
worksheet = workbook['Sheet1']
for counter in range(1, 21):
    content = worksheet["A"+str(counter)].value
    data = {
      "content": content
    }
    json.dumps(data, indent=4, sort_keys=True)
    response = requests.post(url, data=json.dumps(data), headers=headers)
    rescode = response.status_code
    if(rescode != 200):
        print("error happened")
        break
    worksheet["I"+str(counter)] = response.text
    time.sleep(0.5)


workbook.save("self_made_review.xlsx")

