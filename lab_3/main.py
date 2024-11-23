from utils import *
import gradio as gr

iface = gr.Interface(
    fn=main,
    inputs="text",
    outputs=[
        gr.Image(label="График"),
        gr.Textbox(label="Hk(T)"),
        gr.Textbox(label="Hk(T)/k"),
        gr.Textbox(label="Hk(T)/k при k -> inf")
    ],
    title="Частотный анализ текста",
    description="Введите текст для расчета Hk(T)/k для k от 1 до 5 и постройки графика."
)

iface.launch()