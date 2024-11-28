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
    if request.method == "POST":
        # 업로드된 파일 가져오기
        file = request.files.get("file")
        if not file:
            return render_template("index.html", error="No file uploaded!")
        file_path = Path(UPLOAD_FOLDER)/file.filename
        file.save(str(file_path))
        print(file_path)

        print(f"File saved at {file_path}")
        print("Progressing Colorization")

        # DeOldify 컬러화 처리
        result_path = Path(RESULT_FOLDER)/f"{file.filename}"
        try:
            result_path = colorizer.plot_transformed_image(
                path=str(file_path),
                compare=False,
                render_factor=29,
                results_dir=Path(RESULT_FOLDER)
            )
            print(f"Colorization Completed. Result saved at: {result_path}")
        except Exception as e:
            print(f"Colorization Error: {str(e)}")
            return render_template("index.html", error="Colorization Failed!")

        # 결과 반환
        return redirect(url_for("results", filename=file.filename))

    return render_template("index.html")

@app.route("/results/<filename>")
def results(filename):
    print(f"file name is {filename}")
    result_image = f"./results/{filename}"
    return render_template("result.html", result_image=result_image)


if __name__ == "__main__":
    app.run(debug=False)
