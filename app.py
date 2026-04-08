import gradio as gr
from dotenv import load_dotenv
from question_bank_manager import QuestionBankManager

load_dotenv(override=True)

async def run(query: str):
    async for chunk in QuestionBankManager().run(query):
        yield chunk
    

def main():
    with gr.Blocks() as demo:
        gr.Markdown("Please mention the topic of question bank and do mention class & board for which you are generating question bank")
        with gr.Row():
            query_textbox = gr.Textbox(placeholder="Nationalism in India for Class 10 CBSE board")
        btn = gr.Button("Generate")
        question_bank = gr.Markdown(label="Question Bank")
        btn.click(fn=run, inputs=query_textbox, outputs=question_bank)
    demo.launch(inbrowser=True)

if __name__ == "__main__":
    main()
