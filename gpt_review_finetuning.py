from openpyxl import load_workbook
from openpyxl import Workbook
import jsonlines
import json

#jsonl 양식: 
#{“messages”: [{“role”: “system”, “content”: “Marv is a factual chatbot that is also sarcastic.”}, 
# {“role”: “user”, “content”: “What’s the capital of France?”}, 
#{“role”: “assistant”, “content”: “Paris, as if everyone doesn’t know that already.”}]}




review_data = load_workbook("yelp_extract.xlsx")
worksheet = review_data['output']
counter = 0
sampled_data = []
for data_row in worksheet.rows:
    sampled_data.append([data_row[0].value, data_row[1].value]) #[review, user question]

with open("target_data.jsonl", "w", encoding="utf-8") as f:
    for data in sampled_data:
        format_message = {
            "messages" : [
                {
                    "role":"system",
                    "content": "Paid by restaurant, you have to make good reviews of the restaurant."
                },
                {
                    "role":"user",
                    "content":data[1]
                },
                {
                    "role": "assistant",
                    "content": data[0]
                }
            ]
        }

        json.dump(format_message, f, ensure_ascii=False) # ensure_ascii로 한글이 깨지지 않게 저장
        f.write("\n") # json을 쓰는 것과 같지만, 여러 줄을 써주는 것이므로 "\n"을 붙여준다.
    