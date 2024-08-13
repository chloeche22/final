import streamlit as st
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키 가져오기
openai_api_key = os.getenv("OPENAI_API_KEY")

# Streamlit 페이지 구성
st.markdown("# 🌱 기억하는 챗봇")
st.write("이 챗봇은 이전 대화를 기억합니다!")

# LangChain 대화 기억 설정
memory = ConversationBufferMemory()
llm = ChatOpenAI(temperature=0.7, openai_api_key=openai_api_key)  # 여기서 API 키를 전달
conversation = ConversationChain(llm=llm, memory=memory)

# 대화 기록을 저장할 리스트
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 사용자 입력 받기
user_input = st.text_input("나: ", "")

if st.button("보내기"):
    if user_input:
        # 사용자 입력에 대한 챗봇의 응답 생성
        response = conversation.run(user_input)
        
        # 대화 기록에 추가
        st.session_state.chat_history.append(f"나: {user_input}")
        st.session_state.chat_history.append(f"봇: {response}")

# 전체 대화 기록 출력
st.write("## 대화 기록:")
for line in st.session_state.chat_history:
    st.write(line)

# 이전 대화를 초기화할 수 있는 버튼
if st.button("기억 지우기"):
    memory.clear()
    st.session_state.chat_history = []
    st.write("대화 기록과 기억이 초기화되었습니다!")
