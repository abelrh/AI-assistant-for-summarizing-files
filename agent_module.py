# agent_module.py
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()


def generate_full_summary(full_text: str):
    """
    إرسال النص الكامل للمستند إلى Hugging Face مع تمرير التوكن بشكل صارم للنظام.
    """
    # جلب التوكن من الـ Secrets أو الـ .env
    hf_token = st.secrets.get("HF_TOKEN") or os.getenv("HF_TOKEN")

    if not hf_token:
        raise ValueError(
            "لم يتم العثور على HF_TOKEN. أضفه في ملف .env أو إعدادات Secrets."
        )

    # تنظيف التوكن من أي علامات تنصيص أو مسافات بالخطأ
    hf_token = hf_token.strip().replace('"', "").replace("'", "")

    # إجبار النظام على قراءة التوكن بالاسمين الاحتياطيين للمكتبة
    os.environ["HF_TOKEN"] = hf_token
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_token

    # اسم النموذج المستهدف
    repo_id = "Qwen/Qwen2.5-72B-Instruct"

    # تهيئة الـ Endpoint
    llm_endpoint = HuggingFaceEndpoint(
        repo_id=repo_id,
        max_new_tokens=3500,
        temperature=0.5,
        huggingfacehub_api_token=hf_token,  # تمرير مباشر وصريح
    )

    llm = ChatHuggingFace(llm=llm_endpoint)

    # صياغة الـ Prompt (باقي الكود كما هو بدون تغيير)
    system_prompt = """أنت كبير المستشارين ومذيع ومحلل تقني فذ على درجة عالية من الخبرة في تفكيك المستندات والأوراق العلمية المعقدة باللغة العربية.
مهمتك الحالية هي تقديم "قراءة استقصائية تفصيلية ممتدة" للمستند المرفق بالكامل، بأسلوب إذاعي بشري فخم وتفاعلي، بعيداً تماماً عن الاختصار السطحي المخل.

تعليمات صارمة للتحليل والصياغة الفائقة:
1. **المقدمة الإذاعية الفخمة**: ابدأ بترحيب مميز وإثارة للاهتمام حول المستند وطبيعته ومدى تأثيره.
2. **التحليل البنيوي والاستفاضة**: لا تترك فكرة فرعية، أو آلية عمل، أو نتيجة إلا وتقوم بذكرها وشرحها وتفكيكها هندسياً وثنائياً. خذ وقتك ومساحتك الكاملة في الشرح.
3. **الربط السلس والتفاعل البشري**: استخدم عبارات انتقالية ذكية وراقية تزيد من تشويق المستمع وتجعل النص يتدفق كأنه برنامج إذاعي مباشر.
4. **جمالية ونقاء النطق الصوتي**: اكتب بلغة عربية فصحى بالغة الطلاقة والوضوح وقريبة من القلب. تجنب تماماً استخدام التعدادات الجافة أو علامات الماركداون الحادة؛ ادمج كل الأفكار في فقرات نصية سردية غنية وانسيابية.
5. **الخاتمة والأثر**: اختم بقراءة نقدية سريعة للأثر الذي يتركه هذا المستند، تليها خاتمة مقتضبة وشكر وتمنيات بيوم سعيد."""

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            (
                "human",
                "إليك النص الكامل للمستند المرفوع:\n\n{document_text}\n\nقم بصياغة القراءة التحليلية الاستقصائية والمطولة بالكامل الآن بناءً على التعليمات ولا تختصر نهائياً.",
            ),
        ]
    )

    chain = prompt | llm
    result = chain.invoke({"document_text": full_text})
    return result.content
