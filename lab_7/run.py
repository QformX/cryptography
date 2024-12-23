import gradio as gr
from utils import baby_step_giant_step

def find_discrete_log(a, b, p):
    """Находит дискретный логарифм x для a^x ≡ b (mod p)"""
    if b >= p or a >= p:
        return "Неверный ввод: a и b должны быть меньше p."

    result = baby_step_giant_step(a, b, p)
    if result is not None:
        answers, indices, message = result
        output = "Найденные дискретные логарифмы x:\n"
        for x, (i, j) in zip(answers, indices):
            output += f"x = {x} (получено из y_{i} и z_{j})\n"
        return message + output.strip()
    else:
        return "Нет решения для заданных a, b и p."

# Создание интерфейса Gradio
interface = gr.Interface(
    fn=find_discrete_log, 
    inputs=[
        gr.Number(label="Основание (a)", value=2), 
        gr.Number(label="Результат (b)", value=21740), 
        gr.Number(label="Простое модуль (p)", value=30323)
    ],
    outputs="text",
    title="Поиск дискретного логарифма",
    description="Введите значения a, b и p для получения результата a^x ≡ b (mod p)."
)

# Запуск интерфейса
if __name__ == "__main__":
    interface.launch()
