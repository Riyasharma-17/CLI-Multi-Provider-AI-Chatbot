import os
import requests
import gradio as gr

API_URL = "https://cli-multi-provider-ai-chatbot.onrender.com/chat"


def chat(message, history, provider, temperature):
    try:
        response = requests.post(
            API_URL,
            json={
                "message": message,
                "provider": provider.lower(),
                "temperature": temperature,
            },
            timeout=30,
        )

        response.raise_for_status()
        return response.json()["reply"]

    except requests.exceptions.Timeout:
        return "Request timed out. Please try again."

    except requests.exceptions.ConnectionError:
        return "Unable to connect to the backend server."

    except requests.exceptions.HTTPError as e:
        return f"Server Error ({response.status_code}): {e}"

    except Exception as e:
        return f"Unexpected Error: {str(e)}"


custom_css = """
footer {
    display: none;
}

.gradio-container {
    max-width: 980px !important;
    margin: auto;
}

h1 {
    font-weight: 700 !important;
}

.block {
    border-radius: 12px !important;
}
"""

with gr.Blocks(
    title="Multi-Provider AI Chatbot",
    theme=gr.themes.Default(
        primary_hue="gray",
        neutral_hue="slate",
    ),
    css=custom_css,
    fill_width=False,
) as demo:

    gr.Markdown(
        """
# Multi-Provider AI Chatbot

Unified interface for interacting with Groq, Gemini, and OpenRouter through a FastAPI backend.
"""
    )

    with gr.Row():

        provider = gr.Dropdown(
            choices=["Groq", "Gemini", "OpenRouter"],
            value="Groq",
            label="Provider",
        )

        temperature = gr.Slider(
            minimum=0,
            maximum=2,
            value=0.7,
            step=0.1,
            label="Temperature",
        )

    gr.ChatInterface(
        fn=chat,

        additional_inputs=[
            provider,
            temperature,
        ],

        chatbot=gr.Chatbot(
            label="Conversation",
            height=520,
        ),

        textbox=gr.Textbox(
            placeholder="Ask a question...",
            lines=2,
        ),

        examples=[
            ["Explain Docker in one sentence"],
            ["What is LangChain?"],
            ["Write a binary search in Python"],
        ],
    )

    gr.Markdown(
        """
---

Built with FastAPI, LangChain, Gradio, Docker and Render.

Created by **Riya Sharma**
"""
    )


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 7860))

    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False,
        show_error=True,
    )