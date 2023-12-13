import os
import pandas as pd
import schedule
import time
from main import MyPaddleOCR  # 나의 paddleOCR model 불러오기

ocr = MyPaddleOCR()

def process_image(img_path):
    # 이미지 처리 코드 (ocr.run_ocr 등)
    results = ocr.run_ocr(img_path)
    return results

def process_images_in_folder(root_folder):
    # 결과를 저장할 딕셔너리
    all_results = {}

    # root_folder 내의 모든 폴더 가져오기
    categories = [folder for folder in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, folder))]

    # 각 카테고리에 대해 이미지 처리 수행
    for category in categories:
        category_folder = os.path.join(root_folder, category)

        # 폴더 내 모든 파일 가져오기
        file_list = os.listdir(category_folder)
        
        # 이미지 파일들의 경로만 추려내기
        image_paths = [os.path.join(category_folder, file) for file in sorted(file_list) if file.lower().endswith(('.jpg', '.png', '.jpeg'))]

        # 결과를 저장할 리스트
        category_results = []

        # 이미지를 순차적으로 처리
        for img_path in image_paths:
            results = process_image(img_path)
            category_results.append(results)

        # 결과 리스트를 데이터프레임으로 변환
        df = pd.DataFrame(category_results, columns=None)

        # 데이터프레임을 딕셔너리에 저장
        all_results[category] = df

        # 데이터프레임을 CSV 파일로 저장
        csv_path = os.path.join('/home/kchh1015/proj2/all_text_data', f'{category}_results.csv')
        df.to_csv(csv_path, index=False)

    return all_results

def job():
    print("Processing images...")
    root_folder = '/home/kchh1015/proj2/unsarpmask_output_images'
    process_images_in_folder(root_folder)
    print("Images processed.")

# 1달에 한 번 실행되는 스케줄링
schedule.every().month.at("00:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

