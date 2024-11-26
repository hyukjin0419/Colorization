import torch
import torchvision
from deoldify.visualize import *
import warnings
import matplotlib.pyplot as plt
from PIL import Image

# PyTorch 및 torchvision 버전 출력
print("PyTorch version:", torch.__version__)
print("torchvision version:", torchvision.__version__)

# 경고 메시지 무시
warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")

# DeOldify 모델 로드
colorizer = get_image_colorizer(artistic=True)

# 로컬 이미지 경로 및 설정
input_path = "./resource_images/grayRect.png"  # 컬러화할 흑백 이미지 경로
render_factor = 39  # 품질 조정 (7~40)

# 컬러화 수행 및 결과 저장
try:
    result_path = colorizer.plot_transformed_image(
        path=input_path,
        render_factor=render_factor,
        compare=True
    )
    print(f"Colorized image saved to: {result_path}")

    # 컬러화된 이미지 로드 및 표시
    colorized_img = Image.open(result_path)  # 결과 이미지 로드
    plt.figure(figsize=(12, 6))
    plt.title("Colorized Image")
    plt.imshow(colorized_img)
    plt.axis("off")  # 축 숨기기
    plt.show()
except FileNotFoundError:
    print(f"Error: File '{input_path}' not found. Please check the path and try again.")
