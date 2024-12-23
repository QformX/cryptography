import gradio as gr
from utils import *

# Создание интерфейса Gradio
interface = gr.Interface(
    fn=process_message, 
    inputs=[
        gr.Number(label="e", value=251), 
        gr.Number(label="n", value=40349), 
        gr.Number(label="C", value=39620)
    ],
    outputs="text",
    title="RSA Расшифрование",
    description="Введите значения e, n и C для рассчета расшифрованного сообщения."
)

# Запуск интерфейса
interface.launch()
