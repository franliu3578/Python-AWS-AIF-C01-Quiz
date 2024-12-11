import streamlit as st
import json

# 加載 JSON 問題檔案
def load_questions(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# 顯示題目範圍的選擇介面
def interval_quiz_logic(questions):
    # 確保 `questions` 已經是題目列表
    if isinstance(questions, list):
        all_questions = questions  # 直接使用傳入的列表
    else:
        all_questions = load_questions(questions)  # 如果是路徑則讀取 JSON 檔案

    # 全域變數初始化
    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0
    if "selected_questions" not in st.session_state:
        st.session_state.selected_questions = []
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = []
    if "correct_count" not in st.session_state:
        st.session_state.correct_count = 0
    if "interval_selected" not in st.session_state:
        st.session_state.interval_selected = False
    if "quiz_ended" not in st.session_state:
        st.session_state.quiz_ended = False
    if "wrong_answers" not in st.session_state:
        st.session_state.wrong_answers = []

    # 顯示範圍選擇
    if not st.session_state.interval_selected:
        st.title("Select Question interval")
        total_questions = len(all_questions)

        # 提供使用者輸入範圍
        start_index = st.number_input("Start number", min_value=1, max_value=total_questions, value=1)
        end_index = st.number_input("End number", min_value=1, max_value=total_questions, value=total_questions)

        if st.button("Start Quiz"):
            if start_index <= end_index:
                selected_interval= all_questions[start_index - 1:end_index]
                st.session_state.selected_questions = selected_interval
                st.session_state.user_answers = [None] * len(selected_interval)
                st.session_state.current_question_index = 0  # 重置索引
                st.session_state.interval_selected = True  # 標記範圍已選擇
            else:
                st.error("Start number must be less than or equal to end number.")
    elif st.session_state.quiz_ended:  # 如果測驗已結束，顯示總結
        show_quiz_summary()
    else:
        # 顯示練習邏輯
        questions = st.session_state.selected_questions
        current_index = st.session_state.current_question_index
        question = questions[current_index]

        # 顯示問題標題
        st.subheader(f"Question {current_index + 1}: {question['question']}")

        # 如果有程式碼段落，顯示程式碼
        if "code" in question and question["code"]:
            st.code(question["code"], language="python")

        # Handle short answer questions
        if "input_field" in question and question["input_field"]:
            # Multi-line input field
            user_input = st.text_area("Enter your answer:", height=100, key=f"q_{current_index}")
            user_answer = user_input.strip()
        else:
            # Handle single or multiple choice
            if "SELECT TWO" in question["question"].upper() or isinstance(question["answer"], list):
                user_answer = st.multiselect("Choose your answers:", question["options"], key=f"q{current_index}")
            else:
                user_answer = st.radio("Choose your answer:", question["options"], key=f"q{current_index}")

        # 提交按鈕
        if st.button("Submit/Next", key=f"submit_{current_index}"):
            correct_answer = question["answer"]

            # 檢查答案是否正確
            if isinstance(correct_answer, list):
                if set(user_answer) == set(correct_answer):
                    st.success("Correct! 🎉")
                    st.session_state.correct_count += 1
                else:
                    st.error("Incorrect! ❌")
                    record_wrong_answer(current_index, user_answer, question)
            else:
                if user_answer == correct_answer:
                    st.success("Correct! 🎉")
                    st.session_state.correct_count += 1
                else:
                    st.error("Incorrect! ❌")
                    record_wrong_answer(current_index, user_answer, question)

            # 顯示提示
            st.write("### Hint:")
            st.write(f"- **Keywords:** {', '.join(question.get('keywords', []))}")
            st.write(f"- **Explanation:** {question.get('explanation', 'No explanation provided.')}")
            st.markdown("---")

            # 更新題目索引
            if st.session_state.current_question_index < len(questions) - 1:
                st.session_state.current_question_index += 1

        # 加入結束測驗按鈕
        if st.button("End Practice", key="end_practice"):
            st.session_state.quiz_ended = True

# 記錄錯誤答案
def record_wrong_answer(index, user_answer, question):
    original_index = st.session_state.selected_questions[index].get("original_index", index + 1)
    st.session_state.wrong_answers.append({
        "original_index": original_index,
        "question": question["question"],
        "your_answer": user_answer,
        "correct_answer": question["answer"],
        "keywords": question.get("keywords", []),
        "explanation": question.get("explanation", "No explanation provided."),
    })

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
            st.write(f"### Incorrect Question {i} (Original Q{item['original_index']})")
            st.markdown(f"- **Question:** {item['question']}")      
            st.write(f"- **Correct Answer:** {item['correct_answer']}")
            st.write(f"- **Keywords:** {', '.join(item['keywords'])}")
            st.write(f"- **Explanation:** {item['explanation']}")
            st.write(f"- **Your Answer:** {item['your_answer']}")
            st.markdown("---")
