import os
import telebot
from xai_sdk import Client
from xai_sdk.chat import system, user

# 환경변수 불러오기
TELEGRAM_TOKEN = os.getenv("token")
XAI_API_KEY = os.getenv("xai-sdk")  # xai-sdk가 자동으로 읽음

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = Client()  # XAI_API_KEY 자동 사용

# 대화 기록 저장 (재시작하면 초기화됨)
conversations = {}

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    user_id = message.chat.id
    
    if user_id not in conversations:
        conversations[user_id] = client.chat.create(model="grok-4-1-fast-reasoning")
        conversations[user_id].append(system("너는 친절하고 유머러스한 한국어 AI 어시스턴트야. 자연스럽고 도움이 되게 답변해."))
    
    chat = conversations[user_id]
    chat.append(user(message.text))
    
    try:
        response = chat.sample()
        bot.reply_to(message, response.content)
        chat.append(response)  # 대화 유지
    except Exception as e:
        bot.reply_to(message, f"⚠️ 오류: {str(e)}")

print("✅ 봇 시작됨...")
bot.infinity_polling()