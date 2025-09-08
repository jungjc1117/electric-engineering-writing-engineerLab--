import os
from PIL import Image

def resize_canvas_and_pad(input_folder, output_folder, target_height, bg_color=(255, 255, 255)):
    """
    폴더 내 모든 이미지의 캔버스 높이를 특정 픽셀 길이로 늘리고, 
    이미지를 상단에 배치한 후 남는 하단 공간을 흰색으로 채워 새 폴더에 저장합니다.

    Args:
        input_folder (str): 원본 이미지가 저장된 폴더의 경로
        output_folder (str): 처리된 이미지를 저장할 폴더의 경로
        target_height (int): 변경하고자 하는 캔버스의 목표 높이 (픽셀)
        bg_color (tuple): 채워질 배경색 (R, G, B), 기본값은 흰색
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

    print(f"'{input_folder}' 폴더의 이미지를 처리 중...")

    processed_count = 0
    # 폴더 내 파일 목록을 순회
    for filename in os.listdir(input_folder):
        # 파일 확장자가 이미지인지 확인 (대소문자 무시)
        if filename.lower().endswith(supported_extensions):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename)

            try:
                with Image.open(input_file_path).convert("RGB") as img: # PNG의 투명도를 흰색으로 채우기 위해 RGB로 변환
                    original_width, original_height = img.size

                    # 목표 높이가 원본 높이보다 작으면 처리하지 않음 (또는 잘라내기 로직 추가 가능)
                    if target_height < original_height:
                        print(f"경고: '{filename}' 파일의 목표 높이({target_height}px)가 원본 높이({original_height}px)보다 작습니다. 건너뜁니다.")
                        continue
                    
                    # 새 캔버스 생성 (원본 너비, 목표 높이)
                    new_img = Image.new("RGB", (original_width, target_height), bg_color)

                    # 원본 이미지를 새 캔버스 상단에 붙여넣기
                    new_img.paste(img, (0, 0)) # (0, 0)은 좌측 상단 좌표

                    # 새 이미지 저장
                    new_img.save(output_file_path)
                    print(f"'{filename}' 처리 완료 및 '{output_file_path}'에 저장.")
                    processed_count += 1

            except Exception as e:
                print(f"오류: '{filename}' 파일을 처리하는 중 오류가 발생했습니다. ({e})")

    print(f"\n총 {processed_count}개의 이미지 처리가 완료되었습니다.")
    if processed_count == 0:
        print("처리된 이미지가 없거나, 지정된 조건에 맞는 이미지가 없었습니다.")

# --- 사용 예시 ---
# 원본 이미지가 있는 폴더
input_folder_path = '2025_2' 
# 처리된 이미지를 저장할 새 폴더
output_folder_path = '2025_2_padded' 
# 캔버스의 목표 높이 (예: 1000픽셀)
desired_canvas_height = 947 
# 배경색 (선택 사항, 기본값은 흰색)
# bg_color_rgb = (255, 255, 255) # 흰색 (기본값)
# bg_color_rgb = (0, 0, 0)     # 검은색
# bg_color_rgb = (255, 0, 0)   # 빨간색

resize_canvas_and_pad(input_folder_path, output_folder_path, desired_canvas_height)