import os
import base64
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-3.8-flash"


def chat(message: str, history: list[dict]) -> tuple[str, list[dict]]:
    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction="You are a helpful AI assistant. Be concise, friendly, and accurate."
    )
    gemini_history = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [msg["content"]]})

    chat_session = model.start_chat(history=gemini_history)
    response = chat_session.send_message(message)
    reply = response.text
    updated_history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": reply}
    ]
    return reply, updated_history


def analyse_text(text: str, mode: str) -> dict:
    model = genai.GenerativeModel(MODEL)
    word_count = len(text.split())
    if mode == "summarise":
        prompt = f"Summarise this text in 2-3 sentences:\n\n{text}"
    elif mode == "sentiment":
        prompt = f"Analyse the sentiment of this text. Reply with: Positive/Negative/Neutral, then a one-sentence explanation.\n\n{text}"
    elif mode == "keypoints":
        prompt = f"Extract the 3-5 most important key points as a bullet list:\n\n{text}"
    else:
        prompt = f"Analyse this text and provide:\n1. SUMMARY: 2-3 sentences\n2. SENTIMENT: Positive/Negative/Neutral with explanation\n3. KEY POINTS: 3-5 bullet points\n\nText:\n{text}"

    response = model.generate_content(prompt)
    result_text = response.text
    result = {"word_count": word_count}
    if mode == "summarise":
        result["summary"] = result_text
    elif mode == "sentiment":
        result["sentiment"] = result_text
    elif mode == "keypoints":
        result["key_points"] = [l.strip().lstrip("•-* ") for l in result_text.strip().split("\n") if l.strip()]
    else:
        result["summary"] = result_text
        result["sentiment"] = result_text
        result["key_points"] = []
    return result


def analyse_image(image_base64: str, question: str) -> str:
    model = genai.GenerativeModel(MODEL)
    mime_type = "image/jpeg"
    if image_base64.startswith("data:"):
        header, image_base64 = image_base64.split(",", 1)
        if "png" in header: mime_type = "image/png"
        elif "gif" in header: mime_type = "image/gif"
        elif "webp" in header: mime_type = "image/webp"
    image_data = base64.b64decode(image_base64)
    response = model.generate_content([{"mime_type": mime_type, "data": image_data}, question])
    return response.text