# sent_model.py
from transformers import pipeline
import streamlit as st
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

# 감정 분석 함수
def sementic_cls(input, model_name="beomi/KcELECTRA-base"):
    # 파이프라인 생성
    classifier = pipeline("sentiment-analysis", model=model_name)

    # 입력 텍스트 분류
    results = classifier(input)

    # 결과 해석 및 출력
    for result in results:
        label = result['label']
        score = result['score']
        # LABEL_0은 부정적인 감정, LABEL_1은 긍정적인 감정으로 해석
        sentiment = "긍정적인 감정 (Positive)" if label == "LABEL_1" else "부정적인 감정 (Negative)"
        return sentiment, score

# Streamlit 애플리케이션 메인 함수
def main():
    st.title("기억하는 챗봇과 감정 분석기")
    st.write("챗봇과 대화를 나누고 그 대화의 감정을 분석하세요!")

    # .env 파일에서 OpenAI API 키를 가져오기
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if openai_api_key:
        # LangChain 대화 기억 설정
        memory = ConversationBufferMemory()
        llm = ChatOpenAI(temperature=0.7, openai_api_key=openai_api_key)
        conversation = ConversationChain(llm=llm, memory=memory)

        # 대화 기록을 저장할 리스트
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        user_input = st.text_input("텍스트를 입력하세요:")
        if st.button("전송"):
            if user_input:
                # 챗봇 응답 생성
                response = conversation.predict(input=user_input)
                
                # 사용자 입력에 대한 감정 분석
                sentiment, score = sementic_cls(user_input)
                
                # 대화 기록 업데이트
                st.session_state.chat_history.append(f"User: {user_input}")
                st.session_state.chat_history.append(f"Bot: {response}")
                st.session_state.chat_history.append(f"Sentiment: {sentiment}, Score: {score:.4f}")
                
                # 대화 기록 출력
                for chat in st.session_state.chat_history:
                    st.write(chat)
            else:
                st.warning("대화를 입력하세요.")
    else:
        st.error("OpenAI API Key를 설정해주세요.")

if __name__ == "__main__":
    main()
