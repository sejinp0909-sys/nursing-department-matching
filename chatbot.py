
import json
import random
import re
import math

from pathlib import Path
from collections import Counter, defaultdict


# 1. 질문 데이터 불러오기
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data.json"

with open(DATA_FILE, "r", encoding="utf-8") as file:
    question_data = json.load(file)


# 2. 질문을 분석 가능한 단위로 분리
def extract_features(sentence):

    sentence = sentence.lower()
    words = re.findall(r"[가-힣]+|[a-zA-Z]+|\d+", sentence)

    features = []

    for word in words:

        features.append("word:" + word)

        # 두 글자 및 세 글자 단위로 분리
        for n in (2, 3):
            for i in range(len(word) - n + 1):
                features.append(
                    f"char:{word[i:i+n]}"
                )

    return features


# 3. 저장된 질문 목록
saved_questions = [
    item["question"] for item in question_data
]


# 4. 질문별 TF-IDF 벡터 계산
document_count = len(saved_questions)

document_frequency = defaultdict(int)

question_features = []

for question in saved_questions:

    features = extract_features(question)
    feature_count = Counter(features)

    question_features.append(feature_count)

    for feature in feature_count:
        document_frequency[feature] += 1


# 5. TF-IDF 계산
def make_vector(feature_count):

    vector = {}

    total_count = sum(feature_count.values())

    if total_count == 0:
        return vector

    for feature, count in feature_count.items():

        tf = count / total_count

        idf = math.log(
            (document_count + 1) /
            (document_frequency[feature] + 1)
        ) + 1

        vector[feature] = tf * idf

    # 벡터 정규화
    length = math.sqrt(
        sum(value * value for value in vector.values())
    )

    if length > 0:
        for feature in vector:
            vector[feature] /= length

    return vector


question_vectors = [
    make_vector(features)
    for features in question_features
]


# 6. 코사인 유사도 계산
def calculate_similarity(vector_a, vector_b):

    if len(vector_a) > len(vector_b):
        vector_a, vector_b = vector_b, vector_a

    return sum(
        value * vector_b.get(feature, 0)
        for feature, value in vector_a.items()
    )


# 7. 질문 분석 및 답변 반환
def find_answer(user_question):

    if not user_question.strip():
        return "질문을 입력해주세요."

    if not question_data:
        return "등록된 질문 데이터가 없습니다."

    user_features = Counter(
        extract_features(user_question)
    )

    user_vector = make_vector(user_features)

    similarities = [
        calculate_similarity(user_vector, vector)
        for vector in question_vectors
    ]

    best_index = max(
        range(len(similarities)),
        key=lambda i: similarities[i]
    )

    best_score = similarities[best_index]

    # 유사도 기준
    THRESHOLD = 0.18

    if best_score < THRESHOLD:
        return (
            "죄송합니다. 질문과 관련된 답변을 "
            "찾지 못했습니다."
        )

    answer_list = question_data[best_index].get(
        "answers", []
    )

    if not answer_list:
        return "해당 질문에 등록된 답변이 없습니다."

    return random.choice(answer_list)
