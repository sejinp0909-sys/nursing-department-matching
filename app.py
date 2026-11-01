
from flask import Flask, render_template, request, jsonify
from chatbot import find_answer

app = Flask(__name__)


# 메인 채팅 페이지
@app.route("/")
def home():
    return render_template("index.html")


# 사용자 질문 처리
@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    if not data:
        return jsonify({
            "answer": "질문을 입력해주세요."
        }), 400

    user_question = data.get("message", "")

    # 질문 유사도 분석 및 답변 선택
    answer = find_answer(user_question)

    return jsonify({
        "answer": answer
    })


# 서버 실행
if __name__ == "__main__":
    app.run(debug=True)
