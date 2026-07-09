# audio_module.py
import asyncio
import re
import edge_tts
import sys

# إجبار نظام التشغيل والـ Streams في بايثون على اعتماد UTF-8 لتفادي مشاكل الـ ASCII تماماً
if sys.platform.startswith("win"):
    import _locale
    _locale._getdefaultlocale = lambda *args: ("en_US", "utf-8")


def clean_text_for_tts(text: str) -> str:
    """
    تنظيف النص من رموز الـ Markdown (**, #, -, *, إلخ) اللي بيقرأها
    edge_tts حرفياً (زي 'نجمة نجمة') بدل ما يتجاهلها، وتوحيد المسافات
    والأسطر الفارغة عشان الصوت يكمل بسلاسة من غير وقفات أو تكرار.
    """
    # إزالة bold/italic: **نص** أو __نص__ أو *نص* -> نص
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)

    # إزالة عناوين الماركداون # ## ### في أول السطر
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)

    # إزالة علامات البوليت بوينت (-, *, •) في أول السطر
    text = re.sub(r"^[\-\*•]\s+", "", text, flags=re.MULTILINE)

    # إزالة أي نجوم أو رموز تنسيق متبقية منفردة
    text = text.replace("*", "").replace("#", "").replace("`", "")

    # تقسيم على الأسطر، تجاهل الأسطر الفارغة تماماً، ثم دمج الباقي بمسافة واحدة
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]  # skip الأسطر الفاضية
    text = " ".join(lines)

    # توحيد أي مسافات متعددة متبقية لمسافة واحدة
    text = re.sub(r"\s{2,}", " ", text)

    return text.strip()


def text_to_speech_arabic(text: str, output_audio_path: str = "summary_voice.mp3") -> str:
    """
    يحول النص العربي إلى مقطع صوتي تفاعلي وطبيعي بصوت رجل (Microsoft Edge TTS) مجاناً.
    """
    cleaned_text = clean_text_for_tts(text)

    voice = "ar-EG-ShakirNeural"

    async def amain():
        communicate = edge_tts.Communicate(cleaned_text, voice)
        await communicate.save(output_audio_path)

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(amain())
    return output_audio_path