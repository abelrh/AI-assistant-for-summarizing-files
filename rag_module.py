# rag_module.py
from langchain_community.document_loaders import PyPDFLoader

def process_pdf(file_path: str) -> str:
    """
    تقوم بقراءة ملف الـ PDF بالكامل ودمج كافة الصفحات في نص واحد
    لاستغلال نافذة السياق الضخمة لموديل Gemini.
    """
    # 1. تحميل ملف الـ PDF
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # 2. دمج نصوص كافة الصفحات في نص واحد كامل
    full_text = "\n\n".join([doc.page_content for doc in documents])
    return full_text