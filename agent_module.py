# agent_module.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

def generate_full_summary(full_text: str):
    """
    إرسال النص الكامل للمستند إلى Groq (LLaMA 3.3 70B) مباشرة للحصول على تلخيص
    تفاعلي بأسلوب بشري مهيأ للإلقاء الصوتي.
    """
    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "لم يتم العثور على GROQ_API_KEY. "
            "أضفه في ملف .env بالشكل: GROQ_API_KEY=your_key_here"
        )

    # تهيئة موديل Groq بمفتاح الـ API الخاص بك
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.4, # تم رفعها قليلاً لزيادة التفاعلية والطلاقة البشرية في الأسلوب
        api_key=api_key,
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
