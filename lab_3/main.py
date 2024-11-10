from utils import *
import gradio as gr

iface = gr.Interface(
    fn=main,
    inputs="text",
    outputs=["image", "text", "text", "text"],
    title="Частотный анализ текста",
    description="Введите текст для расчета Hk(T)/k для k от 1 до 5 и постройки графика."
)

iface.launch()