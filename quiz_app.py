import streamlit as st
import json

# 加載 JSON 問題檔案
def load_questions(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# 問題文件路徑
questions_file = "python_par2.json"
all_questions = load_questions(questions_file)

# 全域變數初始化
if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0
if "user_answers" not in st.session_state:
    st.session_state.user_answers = []
if "wrong_answers" not in st.session_state:
    st.session_state.wrong_answers = []
if "correct_count" not in st.session_state:
    st.session_state.correct_count = 0
if "show_hint" not in st.session_state:
    st.session_state.show_hint = False
if "range_selected" not in st.session_state:
    st.session_state.range_selected = False
if "selected_questions" not in st.session_state:
    st.session_state.selected_questions = []

# 顯示題目範圍選擇介面
if not st.session_state.range_selected:
    st.title("Select Question Range")
    total_questions = len(all_questions)

    # 輸入範圍
    start_index = st.number_input("Enter start question number (1-based):", min_value=1, max_value=total_questions, value=1)
    end_index = st.number_input("Enter end question number (1-based):", min_value=1, max_value=total_questions, value=total_questions)

    if st.button("Start Quiz"):
        if start_index <= end_index:
            selected_range = all_questions[start_index - 1:end_index]
            st.session_state.selected_questions = [
                {"question": q, "original_index": i + start_index} for i, q in enumerate(selected_range)
            ]  # 保存原始題號
            st.session_state.user_answers = [None] * len(st.session_state.selected_questions)
            st.session_state.range_selected = True
        else:
            st.error("Start question number must be less than or equal to end question number.")
else:
    questions = st.session_state.selected_questions

    def show_question(index):
        question = questions[index]["question"]
        st.subheader(f"Question {index + 1}: {question['question']}")

        # 顯示程式碼區塊（如果有）
        if "code" in question and question["code"]:
            st.code(question["code"], language="python")

        # 動態顯示單選或多選
        if "SELECT TWO" in question["question"].upper():
            user_answer = st.multiselect("Choose your answers:", question["options"], key=f"q{index}")
        else:
            user_answer = st.radio("Choose your answer:", question["options"], key=f"q{index}")

        # 按下按鈕後的行為
        if st.button("Submit/Next", key=f"submit{index}"):
            if not st.session_state.show_hint:
                check_answer(index, user_answer)
                st.session_state.show_hint = True
            else:
                st.session_state.show_hint = False
                if st.session_state.current_question_index < len(questions) - 1:
                    st.session_state.current_question_index += 1
                else:
                    st.success("You have completed the quiz!")

    # 檢查答案並顯示提示
    def check_answer(index, user_answer):
        question = questions[index]["question"]
        correct_answer = question["answer"]
        st.session_state.user_answers[index] = user_answer

        if isinstance(correct_answer, list):  # 多選題
            if set(user_answer) == set(correct_answer):
                st.session_state.correct_count += 1
                st.success("Correct Answer!")
            else:
                record_wrong_answer(index, user_answer)
        else:  # 單選題
            if user_answer == correct_answer:
                st.session_state.correct_count += 1
                st.success("Correct Answer!")
            else:
                record_wrong_answer(index, user_answer)

        st.write("### Hint:")
        st.write(f"- **Keywords:** {', '.join(question['keywords'])}")
        st.write(f"- **Explanation:** {question['explanation']}")
        st.markdown("---")

    def record_wrong_answer(index, user_answer):
        question = questions[index]["question"]
        original_index = questions[index]["original_index"]  # 保存原始題號
        st.session_state.wrong_answers.append({
            "original_index": original_index,
            "question": question["question"],
            "your_answer": user_answer,
            "correct_answer": question["answer"],
            "keywords": question["keywords"],
            "explanation": question["explanation"]
        })
        st.error("Incorrect Answer!")

    # 提交測驗
    def submit_quiz():
        total_questions = len(questions)
        correct_answers = st.session_state.correct_count
        incorrect_answers = len(st.session_state.wrong_answers)
        score = (correct_answers / total_questions) * 100

        st.write(f"### Quiz Summary")
        st.write(f"- Total Questions: {total_questions}")
        st.write(f"- Correct Answers: {correct_answers}")
        st.write(f"- Incorrect Answers: {incorrect_answers}")
        st.write(f"- Score: {score:.2f}%")

        if incorrect_answers == 0:
            st.success("Congratulations! All answers are correct!")
        else:
            st.warning("Some answers were incorrect. Here are the details:")
            for i, item in enumerate(st.session_state.wrong_answers, 1):
                st.write(f"#### Incorrect Question {i} (Original Question {item['original_index']})")
                st.markdown(f"- **Question:** {item['question']}")
                st.write(f"- **Correct Answer:** {item['correct_answer']}")
                st.write(f"- **Keywords:** {', '.join(item['keywords'])}")
                st.write(f"- **Explanation:** {item['explanation']}")
                st.write(f"- **Your Answer:** {item['your_answer']}")
                st.markdown("---")

    # 主程式
    show_question(st.session_state.current_question_index)

    if st.button("Submit Quiz"):
        submit_quiz()
