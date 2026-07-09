# app.py
import streamlit as st
import os
import tempfile

from rag_module import process_pdf
from agent_module import generate_full_summary
from audio_module import text_to_speech_arabic

# إعدادات الصفحة
st.set_page_config(page_title="AI Full PDF Summarizer & Audio Reader", layout="centered")

st.title("🤖 مساعد القراءة الإذاعي التلقائي (Full Text + AI TTS)")
st.write("ارفع ملف الـ PDF الخاص بك، وسيقوم النظام بقراءته بالكامل وتلخيصه بأسلوب بشري تفاعلي وقراءته لك بصوت رجالي طبيعي فوراً!")

# رفع ملف الـ PDF
uploaded_file = st.file_uploader("اختر ملف PDF للتحليل المعمق", type=["pdf"])

if uploaded_file is not None:
    # مفتاح فريد لكل ملف؛ يمنع إعادة التلخيص في كل rerun لصفحة Streamlit
    file_key = f"{uploaded_file.name}_{uploaded_file.size}"

    if st.session_state.get("processed_file_key") != file_key:
        st.session_state["processed_file_key"] = file_key
        st.session_state["final_answer"] = None
        st.session_state["audio_path"] = None

        st.success("تم رفع الملف بنجاح! جاري استخراج النص الكامل للمستند...")

        # حفظ الملف المرفوع مؤقتاً لقراءته
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        try:
            # 1. استخراج النص الكامل من المستند مباشرة
            with st.spinner("جاري قراءة وتحليل المستند بالكامل..."):
                full_text_content = process_pdf(tmp_file_path)

            # 2. إرسال النص بالكامل لـ Gemini لتوليد تلخيص إذاعي بشري وتفاعلي
            with st.spinner("يقوم المستشار الذكي الآن بابتكار ملخص شامل وتفاعلي لك..."):
                final_answer = generate_full_summary(full_text_content)
                st.session_state["final_answer"] = final_answer

            # 3. تحويل التلخيص لصوت رجالي عالي الجودة متوافق مع النصوص الطويلة
            with st.spinner("جاري توليد الصوت الرجالي التفاعلي عالي الجودة..."):
                audio_file_path = text_to_speech_arabic(final_answer)
                st.session_state["audio_path"] = audio_file_path

        except Exception as e:
            st.error(f"حدث خطأ أثناء المعالجة: {str(e)}")
        finally:
            # حذف الملف المؤقت للحفاظ على مساحة المجلد ونظافته
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    # عرض النتائج من الـ session_state
    if st.session_state.get("final_answer"):
        st.subheader("📝 التلخيص التفاعلي المستخرج:")
        st.write(st.session_state["final_answer"])

        if st.session_state.get("audio_path"):
            st.subheader("🔊 الاستماع إلى التلخيص الصوتي (صوت رجالي طبيعي):")
            st.audio(st.session_state["audio_path"], format="audio/mp3")

            with open(st.session_state["audio_path"], "rb") as f:
                st.download_button(
                    label="📥 تحميل الملف الصوتي MP3",
                    data=f,
                    file_name="interactive_summary.mp3",
                    mime="audio/mp3"
                )