import streamlit as st
import json
import os

# 加載 JSON 問題檔案
def load_questions(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# 問題邏輯
def quiz_logic(file_path):
    all_questions = load_questions(file_path)

    # 初始化全域變數
    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = []
    if "wrong_answers" not in st.session_state:
        st.session_state.wrong_answers = []
    if "correct_count" not in st.session_state:
        st.session_state.correct_count = 0
    if "range_selected" not in st.session_state:
        st.session_state.range_selected = False
    if "selected_questions" not in st.session_state:
        st.session_state.selected_questions = []
    if "quiz_ended" not in st.session_state:
        st.session_state.quiz_ended = False

    # 顯示選擇範圍的介面
    if not st.session_state.range_selected:
        st.title("Select Question Range")
        total_questions = len(all_questions)

        start_index = st.number_input("Enter start number (1-based):", min_value=1, max_value=total_questions, value=1)
        end_index = st.number_input("Enter end number (1-based):", min_value=1, max_value=total_questions, value=total_questions)

        if st.button("Start Quiz"):
            if start_index <= end_index:
                selected_range = all_questions[start_index - 1:end_index]
                st.session_state.selected_questions = [
                    {"question": q, "original_index": i + start_index} for i, q in enumerate(selected_range)
                ]
                st.session_state.user_answers = [None] * len(st.session_state.selected_questions)
                st.session_state.range_selected = True
            else:
                st.error("Start question number must be less than or equal to end question number.")
    elif st.session_state.quiz_ended:
        show_quiz_summary()
    else:
        # 顯示目前問題
        show_question(st.session_state.current_question_index)

# 顯示問題
def show_question(index):
    question = st.session_state.selected_questions[index]["question"]
    original_index = st.session_state.selected_questions[index]["original_index"]

    st.subheader(f"Question {index + 1} (Original Index: {original_index})")
    st.write(question["question"])

    # 如果有程式碼段落，顯示程式碼
    if "code" in question and question["code"]:
        st.code(question["code"], language="python")

    # 處理簡答題
    if "input_field" in question and question["input_field"]:
        user_input = st.text_area("Enter your answer:", height=100, key=f"q_{index}")
        user_answer = user_input.strip()
    else:
        # 單選或多選題
        if "SELECT TWO" in question["question"].upper() or isinstance(question["answer"], list):
            user_answer = st.multiselect("Select your answers:", question["options"], key=f"q_{index}")
        else:
            user_answer = st.radio("Select your answer:", question["options"], key=f"q_{index}")

    # 提交答案按鈕
    if st.button("Submit/Next", key=f"submit_{index}"):
        check_answer(index, user_answer)
        if st.session_state.current_question_index < len(st.session_state.selected_questions) - 1:
            st.session_state.current_question_index += 1
        else:
            st.success("You have completed the quiz!")
            st.session_state.quiz_ended = True

    # 提供結束測驗的按鈕
    if st.button("End Quiz", key="end_quiz"):
        st.session_state.quiz_ended = True
        show_quiz_summary()

# 檢查答案
def check_answer(index, user_answer):
    question = st.session_state.selected_questions[index]["question"]
    correct_answer = question["answer"]

    st.session_state.user_answers[index] = user_answer

    # 檢查答案是否正確
    if isinstance(correct_answer, list):  # 多選題
        if set(user_answer) == set(correct_answer):
            st.session_state.correct_count += 1
            st.success("Correct Answer! 🎉")
        else:
            record_wrong_answer(index, user_answer)
    else:  # 單選或簡答題
        if user_answer == correct_answer:
            st.session_state.correct_count += 1
            st.success("Correct Answer! 🎉")
        else:
            record_wrong_answer(index, user_answer)

    # 顯示提示
    st.write("### Hint:")
    st.write(f"- **Keywords:** {', '.join(question.get('keywords', []))}")
    st.write(f"- **Explanation:** {question.get('explanation', 'No explanation provided.')}")
    st.markdown("---")

# 記錄錯誤答案
def record_wrong_answer(index, user_answer):
    question = st.session_state.selected_questions[index]["question"]
    original_index = st.session_state.selected_questions[index]["original_index"]

    st.session_state.wrong_answers.append({
        "original_index": original_index,
        "question": question["question"],
        "your_answer": user_answer,
        "correct_answer": question["answer"],
        "keywords": question.get("keywords", []),
        "explanation": question.get("explanation", "No explanation provided."),
    })
    st.error("Incorrect Answer! ❌")

# 顯示測驗總結
def show_quiz_summary():
    total_questions = len(st.session_state.selected_questions)
    correct_answers = st.session_state.correct_count
    score = (correct_answers / total_questions) * 100

    st.write("## Quiz Summary")
    st.write(f"Total Questions: {total_questions}")
    st.write(f"Correct Answers: {correct_answers}")
    st.write(f"Score: {score:.2f}%")

    if st.session_state.wrong_answers:
        st.warning("Here are your incorrect answers:")
        for i, item in enumerate(st.session_state.wrong_answers, 1):
            st.write(f"### Incorrect Question {i} (Original Question: {item['original_index']})")
            st.markdown(f"- **Question:** {item['question']}")
            st.write(f"- **Correct Answer:** {item['correct_answer']}")
            st.write(f"- **Keywords:** {', '.join(item['keywords'])}")
            st.write(f"- **Explanation:** {item['explanation']}")
            st.write(f"- **Your Answer:** {item['your_answer']}")
            st.markdown("---")
