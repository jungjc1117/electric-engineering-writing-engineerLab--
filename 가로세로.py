import os
from PIL import Image

def print_image_dimensions(folder_path):
    """
    지정된 폴더 내 모든 이미지 파일의 최대 세로 길이를 출력하는 함수

    Args:
        folder_path (str): 이미지가 저장된 폴더의 경로
    """

    # 지원하는 이미지 파일 확장자 목록
    supported_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

    # 폴더가 존재하는지 확인
    if not os.path.isdir(folder_path):
        print(f"오류: '{folder_path}' 폴더를 찾을 수 없습니다.")
        return

    max_height_overall = 0  # 전체 이미지 중 최대 높이를 저장할 변수

    # 폴더 내 파일 목록을 순회
    for filename in os.listdir(folder_path):
        # 파일 확장자가 이미지인지 확인 (대소문자 무시)
        if filename.lower().endswith(supported_extensions):
            file_path = os.path.join(folder_path, filename)

            try:
                # Pillow를 사용해 이미지 열기
                with Image.open(file_path) as img:
                    width, height = img.size
                    
                    # 현재 이미지의 높이가 max_height_overall보다 크면 업데이트
                    if height > max_height_overall:
                        max_height_overall = height

            except Exception as e:
                print(f"오류: {filename} 파일을 여는 중 오류가 발생했습니다. ({e})")

    # 모든 이미지 순회 후 최대 높이 출력
    if max_height_overall > 0:
        print(f"폴더 내 이미지들의 최대 세로 길이: {max_height_overall}px")
    else:
        print("이미지 파일을 찾지 못했거나 처리할 수 없습니다.")


# 사용 예시: '2018_1' 폴더에 이미지가 있다고 가정
image_folder = '2025_2'  # 이 경로를 실제 이미지 폴더 경로로 변경하세요
print_image_dimensions(image_folder)