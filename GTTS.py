import os
import pandas as pd
import time
import schedule
from gtts import gTTS

def process_csv_files(input_folder, output_folder_base):
    # 폴더 내의 모든 CSV 파일 가져오기
    csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

    # 각 CSV 파일에 대해 처리
    for csv_file in csv_files:
        file_path = os.path.join(input_folder, csv_file)
        base_filename = os.path.splitext(os.path.basename(csv_file))[0]

        # 각 CSV 파일에 대한 subfolder 만들기
        output_folder = os.path.join(output_folder_base, base_filename)

        # CSV 파일을 데이터프레임으로 읽어오기
        df = pd.read_csv(file_path)

        # 데이터프레임의 각 행에 대해 처리
        for row in range(8):
            text_to_speak = df['Answer'][row]
            output_path = os.path.join(output_folder, f'voice{row}.mp3')

            # 이미 있는 파일을 확인 후 처리
            if not os.path.exists(output_path):
                # 이미 있다면 저장하지 않음
                tts = gTTS(text=text_to_speak, lang='ko')
                tts.save(output_path)
            else:
                print(f"Using cached audio for row {row} in {csv_file}")

# 사용 예시
input_folder_path = '/home/kchh1015/proj2/Chat_GPT_output'
output_folder_base_path = '/home/kchh1015/proj2/GTTS_output'
process_csv_files(input_folder_path, output_folder_base_path)

def job():
        process_csv_files(input_folder_path, output_folder_base_path)

# Schedule the job to run once a month
schedule.every().month.at('00:00').do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

       