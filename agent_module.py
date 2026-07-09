# agent_module.py
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def generate_full_summary(full_text: str):
    """
    إرسال النص الكامل للمستند إلى Gemini 2.5 Flash مباشرة للحصول على تلخيص
    تفاعلي بأسلوب بشري مهيأ للإلقاء الصوتي.
    """
    # جلب المفتاح أولاً من Secrets (أونلاين) ثم من ملف .env (محلياً)
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("API Key missing! Please set GEMINI_API_KEY in Secrets or .env file.")

    # تهيئة موديل Gemini بالمفتاح الصحيح
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.4,
        api_key=api_key
    )

    # صياغة الـ System Prompt ليكون تفاعلياً ومناسباً لإلقاء رجالي إذاعي ممتع
    system_prompt = """أنت مستشار ومذيع محترف وخبير في تحليل وتلخيص المستندات باللغة العربية.
مهمتك هي قراءة النص الكامل المرفق، ثم صياغة ملخص تنفيذي ممتع للغاية وتفاعلي، وكأنك تشرحه لصديق أو تلقيه في برنامج إذاعي.

تعليمات هامة وأساسية للصياغة:
1. ابدأ بترحيب حار وتفاعلي (مثال: أهلاً بك، يسعدني اليوم أن أقدم لك خلاصة هذا المستند المهم... إلخ).
2. استخدم عبارات انتقالية تفاعلية وجذابة بين الفقرات (مثل: ومن المثير للاهتمام أيضاً..، والآن دعنا ننتقل إلى النقطة الأهم..، وهنا تكمن المفاجأة..).
3. استخرج كافة النقاط والأفكار والنتائج الرئيسية للملف بالكامل دون إهمال أي قسم.
4. اكتب بلغة عربية فصحى مبسطة وقريبة من القلب، وتجنب الرموز المعقدة أو التعدادات الجافة ليكون النص مريحاً وسلساً تماماً عند قراءته صوتياً.
5. اختم الملخص بخاتمة مقتضبة وتفاعلية تعبر عن شكرك."""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "إليك النص الكامل للمستند المرفوع:\n\n{document_text}\n\nقم بصياغة التلخيص التفاعلي الشامل الآن.")
    ])

    chain = prompt | llm
    result = chain.invoke({"document_text": full_text})
    return result.content
