import os
from PIL import Image

def trim_whitespace(input_folder, output_folder, bg_color=(255, 255, 255)):
    """
    폴더 내 이미지에서 지정된 배경색(기본값: 흰색)의 위아래 여백을 제거합니다.

    Args:
        input_folder (str): 원본 이미지가 저장된 폴더의 경로
        output_folder (str): 여백이 제거된 이미지를 저장할 폴더의 경로
        bg_color (tuple): 제거할 배경색 (R, G, B). 기본값은 흰색.
    """

    # 지원하는 이미지 파일 확장자 목록
    supported_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

    # 입력 폴더 존재 여부 확인
    if not os.path.isdir(input_folder):
        print(f"오류: 입력 폴더 '{input_folder}'를 찾을 수 없습니다.")
        return

    # 출력 폴더 생성 (이미 존재하면 만들지 않음)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"출력 폴더 '{output_folder}'를 생성했습니다.")
    else:
        print(f"출력 폴더 '{output_folder}'가 이미 존재합니다.")

    print(f"'{input_folder}' 폴더의 이미지에서 흰색 여백 제거 시작...")

    processed_count = 0
    # 폴더 내 파일 목록을 순회
    for filename in os.listdir(input_folder):
        # 파일 확장자가 이미지인지 확인 (대소문자 무시)
        if filename.lower().endswith(supported_extensions):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename)

            try:
                with Image.open(input_file_path) as img:
                    # RGBA 이미지는 RGB로 변환하여 배경색 처리를 용이하게 합니다.
                    # 투명한 부분은 지정된 bg_color로 채웁니다.
                    if img.mode == 'RGBA':
                        temp_img = Image.new("RGB", img.size, bg_color)
                        temp_img.paste(img, mask=img.split()[3]) # 알파 채널을 마스크로 사용
                        img = temp_img
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    width, height = img.size
                    
                    # 이미지의 경계 상자(bounding box)를 찾습니다.
                    # 흰색 픽셀이 아닌 첫 번째 픽셀을 기준으로 좌표를 계산합니다.
                    
                    # 위쪽 흰색 여백 제거
                    top = 0
                    while top < height:
                        # 현재 행의 모든 픽셀이 배경색과 일치하는지 확인
                        if all(img.getpixel((x, top)) == bg_color for x in range(width)):
                            top += 1
                        else:
                            break

                    # 아래쪽 흰색 여백 제거
                    bottom = height - 1
                    while bottom >= top:
                        # 현재 행의 모든 픽셀이 배경색과 일치하는지 확인
                        if all(img.getpixel((x, bottom)) == bg_color for x in range(width)):
                            bottom -= 1
                        else:
                            break

                    # 왼쪽/오른쪽 여백도 제거하고 싶다면 유사한 로직을 추가하면 됩니다.
                    # 여기서는 위아래만 처리합니다.

                    # 잘라낼 영역을 결정합니다. (top, left, bottom, right)
                    # left와 right는 원본 이미지의 전체 너비로 유지됩니다.
                    if top < height and bottom >= top:
                        bbox = (0, top, width, bottom + 1) # bottom + 1은 slice의 끝점이 포함되지 않기 때문
                        trimmed_img = img.crop(bbox)
                        
                        # 결과 이미지 저장
                        trimmed_img.save(output_file_path)
                        print(f"'{filename}'의 위아래 여백 제거 완료 및 '{output_file_path}'에 저장.")
                        processed_count += 1
                    else:
                        print(f"'{filename}' 파일은 흰색만으로 구성되어 있거나 처리할 여백이 없습니다. 건너뜁니다.")

            except Exception as e:
                print(f"오류: '{filename}' 파일을 처리하는 중 오류가 발생했습니다. ({e})")

    print(f"\n총 {processed_count}개의 이미지 처리가 완료되었습니다.")
    if processed_count == 0:
        print("처리된 이미지가 없거나, 지정된 조건에 맞는 이미지가 없었습니다.")

# --- 사용 예시 ---
# 원본 이미지가 있는 폴더
input_folder_path = '2025_2_padded-merged' 
# 여백 제거 후 이미지를 저장할 새 폴더
output_folder_path = '2025_2_padded-merged_trimmed' 
# 제거할 배경색 (예: 흰색. 다른 색이면 이 값을 변경하세요)
# bg_color_to_remove = (255, 255, 255) # 흰색 (기본값)
# bg_color_to_remove = (0, 0, 0)     # 검은색
# bg_color_to_remove = (255, 0, 0)   # 빨간색

# 흰색 여백 제거 실행
trim_whitespace(input_folder_path, output_folder_path)

# 만약 다른 색상의 여백을 제거하고 싶다면, bg_color_to_remove 값을 변경하여 함수를 다시 호출합니다.
# 예: 검은색 여백 제거
# trim_whitespace(input_folder_path, 'output_images_trimmed_black_bg', bg_color=(0, 0, 0))