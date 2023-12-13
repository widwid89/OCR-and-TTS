import os
import cv2
import schedule
import time

def preprocess_image(image_path, output_folder):
    # 이미지 불러오기
    img = cv2.imread(image_path)

    # 그레이스케일 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 블러 처리
    blurred_image = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 언샵 마스크 처리
    unsharp_mask = cv2.addWeighted(gray, 2.5, blurred_image, -1.5, 0)

    # 결과 이미지 저장 (확장자 변경)
    file_name = os.path.basename(image_path)
    output_name, ext = os.path.splitext(file_name)
    output_path = os.path.join(output_folder, f"{output_name}_preprocessed.jpeg")

    cv2.imwrite(output_path, unsharp_mask)

def process_images_in_folder(input_folder, output_base_folder):
    # 폴더 내 모든 파일 가져오기
    file_list = os.listdir(input_folder)

    # 이미지 파일들의 경로만 추려내기
    image_paths = [os.path.join(input_folder, file) for file in file_list if file.lower().endswith(('.jpg', '.png', '.jpeg'))]

    # 결과 이미지를 저장할 디렉터리 경로
    output_folder = os.path.join(output_base_folder, os.path.basename(input_folder))
    os.makedirs(output_folder, exist_ok=True)

    # 이미지를 순차적으로 처리
    for img_path in image_paths:
        preprocess_image(img_path, output_folder)


def process_all_folders():
    folders_to_process = {'/home/kchh1015/proj2/superres_output_images/과자/': '/home/kchh1015/proj2/unsarpmask_output_images/과자/',
                      '/home/kchh1015/proj2/superres_output_images/건강식품/': '/home/kchh1015/proj2/unsarpmask_output_images/건강식품/',
                      '/home/kchh1015/proj2/superres_output_images/면류/': '/home/kchh1015/proj2/unsarpmask_output_images/면류/',
                      '/home/kchh1015/proj2/superres_output_images/생수/': '/home/kchh1015/proj2/unsarpmask_output_images/생수/',
                      '/home/kchh1015/proj2/superres_output_images/김치/': '/home/kchh1015/proj2/unsarpmask_output_images/김치/',
                      '/home/kchh1015/proj2/superres_output_images/베이커리/': '/home/kchh1015/proj2/unsarpmask_output_images/베이커리/',
                      '/home/kchh1015/proj2/superres_output_images/양념/': '/home/kchh1015/proj2/unsarpmask_output_images/양념/',
                      '/home/kchh1015/proj2/superres_output_images/우유/': '/home/kchh1015/proj2/unsarpmask_output_images/우유/',
                      '/home/kchh1015/proj2/superres_output_images/커피/': '/home/kchh1015/proj2/unsarpmask_output_images/커피/',
                      '/home/kchh1015/proj2/superres_output_images/밀키트/': '/home/kchh1015/proj2/unsarpmask_output_images/밀키트/',}


    model_path = "/home/kchh1015/proj2/FSRCNN_Tensorflow/models/FSRCNN_x2.pb"
    scale_factor = 2

    for input_folder, output_base_folder in folders_to_process.items():
        process_images_in_folder(input_folder, output_base_folder)

def job():
    print("Processing images...")
    process_all_folders()
    print("Images processed.")

# 1달에 한 번 실행되는 스케줄링
schedule.every().month.at("00:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
