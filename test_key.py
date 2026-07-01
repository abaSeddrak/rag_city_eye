
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(f"🔑 API Key: {api_key[:20]}...")

try:
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    response = llm.invoke("مرحبا! كيف حالك؟")
    print(f"✅ الـ API key شغال!")
    print(f"💬 Response: {response.content}")
except Exception as e:
    print(f"❌ الـ API key غلط أو مفيش internet")
    print(f"Error: {str(e)}")
