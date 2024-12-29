import gradio as gr
from utils import *

# Импортируйте ваши функции для факторизации...

def quadratic_sieve_interface(m, a, b, c):
    result = sieve_factorization(m, a, b, c)
    if result[0] is not None:
        return f"Число {m} факторизуется как: {result[0]} * {result[1]}"
    else:
        return "Не удалось найти делители с использованием квадратичного решета."

def rho_method_interface(m, x0, y0):
    divisor = rho_method(m, x0, y0)
    if divisor:
        return f"Найден делитель: {divisor}"
    else:
        return "Не удалось найти делитель с использованием ρ-метода."

def create_gradio_interface():
    with gr.Blocks() as demo:
        gr.Markdown("# Факторизация чисел")
        
        with gr.Tab("Квадратичное решето"):
            m_input = gr.Number(label="Введите число m", value=42)
            a_input = gr.Number(label="Введите модуль a", value=2)
            b_input = gr.Number(label="Введите модуль b", value=3)
            c_input = gr.Number(label="Введите модуль c", value=5)
            calculate_button = gr.Button("Факторизовать")
            result_output = gr.Textbox(label="Результат", interactive=False)

            calculate_button.click(
                quadratic_sieve_interface,
                inputs=[m_input, a_input, b_input, c_input],
                outputs=result_output
            )
        
        with gr.Tab("ρ-метод"):
            m_rho_input = gr.Number(label="Введите число m", value=42)
            x0_input = gr.Number(label="Введите начальное значение x0", value=1)
            y0_input = gr.Number(label="Введите начальное значение y0", value=1)
            rho_calculate_button = gr.Button("Факторизовать")
            rho_result_output = gr.Textbox(label="Результат", interactive=False)

            rho_calculate_button.click(
                rho_method_interface,
                inputs=[m_rho_input, x0_input, y0_input],
                outputs=rho_result_output
            )

    return demo

if __name__ == "__main__":
    interface = create_gradio_interface()
    interface.launch()
