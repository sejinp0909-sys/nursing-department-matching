
import json
import random

from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# 1. 저장된 데이터 불러오기
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data.json"

with open(DATA_FILE, "r", encoding="utf-8") as file:
    question_data = json.load(file)


# 2. 문장 유사도 분석 모델 불러오기
model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)


# 3. 저장된 질문 목록 만들기
saved_questions = [
    item["question"] for item in question_data
]


# 4. 저장된 질문을 미리 벡터로 변환하기
question_vectors = model.encode(saved_questions)


# 5. 질문 분석 함수
def find_answer(user_question):

    # 빈 질문 확인
    if not user_question.strip():
        return "질문을 입력해주세요."

    # 사용자가 입력한 문장을 벡터로 변환
    user_vector = model.encode([user_question])

    # 저장된 질문들과 유사도 계산
    similarities = cosine_similarity(
        user_vector,
        question_vectors
    )[0]

    # 가장 유사한 질문의 위치 찾기
    best_index = similarities.argmax()

    # 가장 높은 유사도 점수
    best_score = similarities[best_index]

    # 유사도 기준 설정
    THRESHOLD = 0.45

    # 유사도가 기준보다 낮으면 답변하지 않음
    if best_score < THRESHOLD:
        return "죄송합니다. 질문과 관련된 답변을 찾지 못했습니다."

    # 가장 유사한 질문의 답변 목록 가져오기
    answer_list = question_data[best_index]["answers"]

    # 답변이 없는 경우
    if not answer_list:
        return "해당 질문에 등록된 답변이 없습니다."

    # 여러 답변 중 하나 무작위 선택
    selected_answer = random.choice(answer_list)

    return selected_answer
