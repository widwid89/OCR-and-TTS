import openai
import schedule
import time
import pandas as pd
import os

# 발급받은 API 키 설정
OPENAI_API_KEY = "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"

# openai API 키 인증
openai.api_key = OPENAI_API_KEY

model = "gpt-3.5-turbo"

previous_answer = '''1kg 9g의 아카시아 벌꿀로, 국산 아카시아 벌꿀 100%를 사용하였습니다. 탄소동위원소 -235%를 가지며, 뚜껑은 폴리프로필렌PP와 폴리에틸렌테레이프탈레이트PET로 만들었습니다. 소분원은 경기도 안성시의 주허니스티이며, 판매원은 서울특별시 성동구 이마트입니다.

사용 주의사항:
1세 미만의 영아에게는 섭취를 자제하고, 직사광선을 피해 실온에서 보관하며 냉장고에는 보관하지 않도록 권고합니다. 벌꿀의 결정화는 자연스러운 현상으로 물에 넣어 녹이는 것을 권장하며, 끓이지 말아야 합니다.

기타 사항:
이 제품은 소비자분쟁해결 기준에 따라 교환 및 환불이 가능하며, 반품 및 교환은 구입처 및 소분원에서 가능합니다. 부정불량 식품 신고는 국번 없이 1399로 가능합니다.

원료성분 및 영양정보:

원료성분: 아카시아 벌꿀 100%
영양정보: 정보 없음'''

previous_answer1 = '''1킬로그램 9그램의 국산 아카시아 벌꿀로 만든 제품으로, 탄소동위원소 -235%를 가지며 폴리프로필렌PP와 
폴리에틸렌테레이프탈레이트PET로 된 뚜껑을 사용하였습니다; 1세 미만 영아에게는 섭취를 자제하고 직사광선을 피해 실온에서 보관하며, 
냉장고에는 보관하지 않도록 권고하며, 벌꿀의 결정화는 물에 넣어 녹이는 것을 권장하며 끓이지 말아야 합니다. 교환 및 환불은 소비자분쟁해결 
기준에 따라 가능하며, 반품 및 교환은 구입처 및 소분원에서 가능하며, 부정불량 식품 신고는 국번 없이 1399로 가능합니다.'''


def process_and_summarize_csv(csv_folder):
    # List all CSV files in the folder
    csv_files = [file for file in os.listdir(csv_folder) if file.endswith('.csv')]
    
    # Loop through each CSV file
    for csv_file in csv_files:
        # Load CSV file into a dataframe
        df = pd.read_csv(os.path.join(csv_folder, csv_file))

        # Create an empty dataframe to store the results for this CSV file
        results_df = pd.DataFrame(columns=['Answer'])
        df = pd.DataFrame(df.apply(lambda row: '  '.join(map(str, row)), axis=1))
        
        # Loop through each row in the dataframe
        for index, row in df.iterrows():
            # Extract text from the desired column (adjust 'column_name' accordingly)
            text = row[0]

            # Construct the chat messages
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "assistant", "content": previous_answer},
                {"role": "assistant", "content": previous_answer1},
                {"role": "user", "content": text + """위 텍스트를 nan값을 빼고 글을 자세하게 요약해주고 원료성분과 영양정보를 구체적으로 알려줘. 
                 만약에 원료성분과 영양성분에 대한 정보가 없다면 이 2개의 요소는 빼고 요약본만 적어줘. 또한 업소명, 소재지, 소분원 같은 내용은 빼줘. 그리고 영양
                 성분에서 kcal나 mg 같은 영어로 된 단위 및 모든 숫자를 한글로 대체해줘."""}]

            # Request completion from OpenAI API
            response = openai.ChatCompletion.create(model=model, messages=messages)
            answer = response['choices'][0]['message']['content']

            # Append the results to the dataframe
            results_df = results_df.append({
                'Answer': answer
            }, ignore_index=True)

        # Save the results dataframe to a CSV file for this input CSV
        results_csv_path = f'/home/kchh1015/proj2/Chat_GPT_output/{csv_file}_results.csv'
        results_df.to_csv(results_csv_path, index=False)

def job():
    print("Processing and summarizing CSV files...")
    csv_folder = '/home/kchh1015/proj2/all_text_data'
    process_and_summarize_csv(csv_folder)
    print("CSV files processed and summarized.")

# 1달에 한 번 실행되는 스케줄링
schedule.every().month.at("00:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)


