from flask import Flask, render_template, request, send_file,redirect, url_for
from deoldify.visualize import *
import os
import matplotlib
from pathlib import Path

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

@app.route("/uploads", methods=["POST"])
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


if __name__ == "__main__":
    app.run(debug=False)
