import os
from PIL import Image

# 원본 이미지 폴더 경로
input_folder = "./2025_2_padded"   # 👉 여기에 원본 이미지 폴더 경로 입력
# 합쳐진 이미지를 저장할 폴더
output_folder = "./2025_2_padded-merged"

# 저장 폴더 없으면 생성
os.makedirs(output_folder, exist_ok=True)

# 이미지 파일 이름 정렬 (01.png, 02.png ... 순서대로)
files = sorted([f for f in os.listdir(input_folder) if f.lower().endswith(".png")])

# 두 장씩 묶어서 처리
for i in range(0, len(files), 2):
    if i+1 >= len(files):
        break  # 홀수 개일 경우 마지막 이미지는 건너뜀

    file1 = os.path.join(input_folder, files[i])
    file2 = os.path.join(input_folder, files[i+1])

    img1 = Image.open(file1)
    img2 = Image.open(file2)

    # 두 이미지의 세로 크기 중 큰 값으로 맞추기
    max_height = max(img1.height, img2.height)

    # 비율 유지하면서 세로 크기 맞춤
    def resize_to_height(img, target_height):
        ratio = target_height / img.height
        new_width = int(img.width * ratio)
        return img.resize((new_width, target_height), Image.LANCZOS)

    img1_resized = resize_to_height(img1, max_height)
    img2_resized = resize_to_height(img2, max_height)

    # 두 이미지를 가로로 이어붙일 새 캔버스 생성
    total_width = img1_resized.width + img2_resized.width
    merged = Image.new("RGB", (total_width, max_height), (255, 255, 255))

    # 왼쪽/오른쪽에 붙이기
    merged.paste(img1_resized, (0, 0))
    merged.paste(img2_resized, (img1_resized.width, 0))

    # 저장 파일 이름 (예: merge_01_02.png)
    output_name = f"merge_{files[i][:-4]}_{files[i+1][:-4]}.png"
    merged.save(os.path.join(output_folder, output_name))

    print(f"저장 완료: {output_name}")

print("✅ 모든 이미지 병합 완료!")
