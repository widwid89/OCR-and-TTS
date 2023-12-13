import os
import cv2
import schedule
import time

def superres_upsample(input_image_path, output_image_path, model_path, scale_factor):
    # 이미지 불러오기
    img = cv2.imread(input_image_path)
    print(img.shape)

    # Super-Resolution 모델 초기화
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(model_path)
    sr.setModel("fsrcnn", scale_factor)

    # 이미지 업샘플링
    result = sr.upsample(img)
    print(result.shape)
    print(result.dtype)


    # 결과 이미지 저장
    cv2.imwrite(output_image_path, result)

def preprocess_images_in_folder(input_folder, output_folder, model_path, scale_factor):
    # 입력 폴더 내의 모든 이미지 파일 가져오기
    image_files = [f for f in os.listdir(input_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

    # 각 이미지에 대해 전처리 수행
    for image_file in image_files:
        input_image_path = os.path.join(input_folder, image_file)

        # 새로운 파일명 생성
        output_image_name = f"{os.path.splitext(image_file)[0]}_superres.jpg"
        output_image_path = os.path.join(output_folder, output_image_name)

        # Super-Resolution 적용 및 결과 이미지 저장
        superres_upsample(input_image_path, output_image_path, model_path, scale_factor)


def process_all_folders():
    folders_to_process = {
        '/home/kchh1015/proj2/Dataset/건강식품/': '/home/kchh1015/proj2/superres_output_images/건강식품/',
        '/home/kchh1015/proj2/Dataset/생수/': '/home/kchh1015/proj2/superres_output_images/생수/',
        '/home/kchh1015/proj2/Dataset/면류/': '/home/kchh1015/proj2/superres_output_images/면류/',
        '/home/kchh1015/proj2/Dataset/과자/': '/home/kchh1015/proj2/superres_output_images/과자/',
        '/home/kchh1015/proj2/Dataset/김치/': '/home/kchh1015/proj2/superres_output_images/김치/',
        '/home/kchh1015/proj2/Dataset/베이커리/': '/home/kchh1015/proj2/superres_output_images/베이커리/',
        '/home/kchh1015/proj2/Dataset/양념/': '/home/kchh1015/proj2/superres_output_images/양념/',
        '/home/kchh1015/proj2/Dataset/우유/': '/home/kchh1015/proj2/superres_output_images/우유/',
        '/home/kchh1015/proj2/Dataset/커피/': '/home/kchh1015/proj2/superres_output_images/커피/',
        '/home/kchh1015/proj2/Dataset/밀키트/': '/home/kchh1015/proj2/superres_output_images/밀키트/'
    }

    model_path = "/home/kchh1015/proj2/FSRCNN_Tensorflow/models/FSRCNN_x2.pb"
    scale_factor = 2

    for input_folder, output_base_folder in folders_to_process.items():
        preprocess_images_in_folder(input_folder, output_base_folder, model_path, scale_factor)

def job():
    print("Processing images...")
    process_all_folders()
    print("Images processed.")

# 1달에 한 번 실행되는 스케줄링
schedule.every().month.at("00:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)


