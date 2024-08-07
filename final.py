import streamlit as st
import pandas as pd

# 할 일 목록을 저장할 데이터프레임 생성
if 'todo_list' not in st.session_state:
    st.session_state.todo_list = pd.DataFrame(columns=['Task', 'Status'])

def add_task(task):
    # 새로운 할일을 추가
    # 이때 pd.concat 으로 기존 todo_list 에 추가해줘야함
     new_task =pd.DataFrame([task,"pending"],columns=['Task','status'])
    pd.concat([st.session_stae.todo_list, new_task])
 
def delete_task(index):
    st.session_state.todo_list.drop(index, inplace=True)
    st.session_state.todo_list.reset_index(drop=True, inplace=True)

def mark_task_complete(index):
    st.session_state.todo_list.at[indes,'status'] = "completed"
    # index 에 해당하는 status 변경하기

def main():
    st.title("할 일 관리 도구")
    st.write("오늘의 할 일을 추가하고 관리하세요.")

    # 할 일 추가
    new_task = st.text_input("할 일 입력")
    if st.button("추가"):
        if new_task:
            add_task(new_task)
            st.success(f"'{new_task}' 추가됨")
            else:
            st.warning("할 일을 입력하세요.")

    # 할 일 목록 표시
    st.subheader("할 일 목록")
    if st.session_state.todo_list.empty:
        st.write("현재 할 일이 없습니다.")
        
    else:
        for index, row in st.session_state.todo_list.iterrows():
            col1, col2, col3 = st.columns([6, 1, 1])
            col1.write(row['Task'])
            if row['Status'] == "Pending":
                if col2.button("완료", key=f"complete_{index}"):
                    mark_task_complete(index)
                    st.experimental_rerun()
            else:
                col2.write("완료됨")
                
            if col3.button("삭제", key=f"delete_{index}"):
                delete_task(index)
                st.experimental_rerun()

if __name__ == "__main__":
    main()

