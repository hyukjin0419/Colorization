from flask import Flask, render_template, request, send_file,redirect, url_for
from deoldify.visualize import *
import os
import matplotlib
from pathlib import Path
import cv2

matplotlib.use('Agg')


# Flask 앱 생성
app = Flask(__name__)

# 업로드와 결과 디렉토리 생성
UPLOAD_FOLDER = "./static/uploads"
RESULT_FOLDER = "./static/results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# DeOldify 모델 로드
colorizer = get_image_colorizer(artistic=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/result", methods=["POST"])
def uploads():
    # 업로드된 파일 가져오기
    file = request.files.get("file")
    if not file:
        return render_template("index.html", error="No file uploaded!")
    # 업로드된 파일 저장하기
    file_path = Path(UPLOAD_FOLDER)/file.filename
    file.save(str(file_path))
    print(f"File saved at {file_path}")

    #변환 작업 후 저장하기
    try:
        result_path = colorizer.plot_transformed_image(
            path = Path(file_path),
            compare=False,
            render_factor = 29,
            results_dir = Path(RESULT_FOLDER)
        )
        print(f"Colorization complete at {result_path}")
    except Exception as e:
        print("Colorization Error")
        return redirect(url_for("index",error="Colorization Error"))
    
    result_file_url = f"results/{file.filename}"
    return render_template("result.html",result_file_url = result_file_url)

#해상도 부분
def upscale_image(input_path, output_path, scale=2):
    target_image = cv2.imread(str(input_path))
    sr = dnn_superres.DnnSuperResImpl_create()
    path = './models/EDSR_x3.pb'
    sr.readModel(path)
    sr.setModel('edsr', 3)
    upscaled = sr.upsample(target_image)
    cv2.imwrite(output_path, upscaled)

#해상도 개선
@app.route("/enhance/<filename>", methods=["GET"])
def enhance_image(filename):
    input_path = Path(RESULT_FOLDER) / filename
    output_path = Path(RESULT_FOLDER) / f"enhanced_{filename}"

    try:
        # 이미지 해상도 개선
        upscale_image(input_path, output_path, scale=2)
        return render_template("result.html", result_file_url=f"results/enhanced_{filename}")
    except Exception as e:
        print(f"Enhancement error: {e}")
        return redirect(url_for("index"))

        
if __name__ == "__main__":
    app.run(debug=False)


#다운로드 버튼 추가해야함
#버퍼링 만들어야 함
#그 다음 비디오로 넘어가기
#흐음.....
#아 파일 확장자 제한해야함