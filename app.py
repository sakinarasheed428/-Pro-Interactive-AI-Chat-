# ============================================
# 🤍 PRO INTERACTIVE AI CHAT 😎🔥
# Top Input • Light Theme • Side Settings
# ============================================

import os
import time
import gradio as gr
from groq import Groq

# 🔐 PUT YOUR GROQ API KEY HERE
os.environ["GROQ_API_KEY"] = ""

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

conversation_memory = []

# -------------------------------
# AI FUNCTION
# -------------------------------
def get_ai_response(message, mode, target_language):
    global conversation_memory

    if mode == "🌍 Translator":
        prompt = f"Translate this text into {target_language} naturally:\n\n{message}"
    else:
        prompt = message

    conversation_memory.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a smart, friendly AI assistant. Use light emojis 😊 and keep replies professional."
            }
        ] + conversation_memory,
        temperature=0.6
    )

    reply = response.choices[0].message.content.strip()
    conversation_memory.append({"role": "assistant", "content": reply})

    return reply

# -------------------------------
# TYPING EFFECT
# -------------------------------
def chatbot_response(message, history, mode, language):
    history = history or []

    history.append((message, "🤖 Typing..."))
    yield history

    time.sleep(0.4)

    full_reply = get_ai_response(message, mode, language)

    animated = ""
    for char in full_reply:
        animated += char
        history[-1] = (message, animated)
        time.sleep(0.008)
        yield history

# -------------------------------
# CLEAR CHAT
# -------------------------------
def clear_chat():
    global conversation_memory
    conversation_memory = []
    return []

# -------------------------------
# UI DESIGN
# -------------------------------
custom_css = """
body {background-color: #f4f8fb;}
.gradio-container {background-color: #f4f8fb;}
"""

with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:

    gr.Markdown("## 💎 Pro Interactive AI Chat 😎")

    with gr.Row():

        # LEFT SETTINGS PANEL
        with gr.Column(scale=1):
            gr.Markdown("### ⚙ Settings")

            mode = gr.Radio(
                ["💬 Chat","🌍 Translator"],
                value="💬 Chat",
                label="Mode"
            )

            language = gr.Dropdown(
                ["English","Urdu","French","Spanish","German","Arabic","Chinese","Hindi"],
                value="English",
                label="Translate To"
            )

            clear = gr.Button("🔄 New Chat")

        # RIGHT MAIN CHAT
        with gr.Column(scale=3):

            # 🔥 TOP MESSAGE INPUT
            with gr.Row():
                msg = gr.Textbox(
                    placeholder="Type your message here 😎",
                    show_label=False,
                    scale=4
                )

                send = gr.Button("Send 🚀", scale=1)

            chatbot = gr.Chatbot(height=500)

    send.click(
        chatbot_response,
        inputs=[msg, chatbot, mode, language],
        outputs=chatbot
    )

    msg.submit(
        chatbot_response,
        inputs=[msg, chatbot, mode, language],
        outputs=chatbot
    )

    clear.click(clear_chat, outputs=chatbot)

demo.launch(share=True)
