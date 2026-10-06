from flask import Flask, render_template, request

app = Flask(__name__)


# 첫 화면
@app.route("/")
def home():
    return render_template("index.html")


# 질문 화면
@app.route("/question")
def question():
    return render_template("question.html")


# 결과 계산
@app.route("/result", methods=["POST"])
def result():

    # 부서별 점수
    scores = {
        "병동": 0,
        "응급실": 0,
        "중환자실": 0,
        "수술실": 0
    }

    # 20개의 질문에서 선택한 답을 가져옴
    for i in range(1, 21):

        answer = request.form.get(f"q{i}")

        if answer:
            scores[answer] += 1

    # 가장 높은 점수의 부서 찾기
    sorted_scores = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    first_department = sorted_scores[0][0]
    second_department = sorted_scores[1][0]

    return render_template(
        "result.html",
        first_department=first_department,
        second_department=second_department,
        scores=scores
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)