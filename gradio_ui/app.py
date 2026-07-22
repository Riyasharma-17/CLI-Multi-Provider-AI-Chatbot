import gradio as gr
import requests

API_URL = "https://cli-multi-provider-ai-chatbot.onrender.com/chat"


def chat(message, history, provider, temperature):
    try:
        response = requests.post(
            API_URL,
            json={
                "message": message,
                "provider": provider.lower(),
                "temperature": temperature
            },
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        return data["reply"]

    except requests.exceptions.Timeout:
        return "⏳ Request timed out. The server is taking too long to respond."

    except requests.exceptions.ConnectionError:
        return "❌ Unable to connect to the backend server."

    except requests.exceptions.HTTPError as e:
        return f"⚠️ Server Error ({response.status_code}): {e}"

    except Exception as e:
        return f"❌ Unexpected Error: {str(e)}"


with gr.Blocks(title="Multi-Provider AI Chatbot") as demo:

    gr.Markdown(
        """
# 🤖 Multi-Provider AI Chatbot

Chat with **Groq**, **Gemini**, or **OpenRouter** through a unified **FastAPI + LangChain** backend.

Choose a provider, adjust the temperature, and start chatting!
"""
    )

    provider = gr.Dropdown(
        choices=["Groq", "Gemini", "OpenRouter"],
        value="Groq",
        label="LLM Provider"
    )

    temperature = gr.Slider(
        minimum=0,
        maximum=2,
        value=0.7,
        step=0.1,
        label="Temperature"
    )

    gr.ChatInterface(
        fn=chat,
        additional_inputs=[
            provider,
            temperature
        ]
    )

    gr.Markdown(
        """
---
### 🛠 Built With

- ⚡ FastAPI
- 🦜 LangChain
- 🤖 Gradio
- 🐳 Docker
- ☁️ Render
"""
    )

demo.launch()