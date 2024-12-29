from utils import *
import gradio as gr

print(system_lin_con(5,0,6,3,7))

with gr.Blocks() as app:
    
    gr.Markdown("# Алгоритм аффинного шифрования")

    with gr.Tab("НОД и коэффициенты Безу"):
        with gr.Row():
            element = gr.Number(label="Первое число")
            mod = gr.Number(label="Второе число")
            output_inv = gr.Textbox(label="(НОД, коэф, коэф)", interactive=False)
        gr.Button("Вычислить").click(extended_gcd, inputs=[element, mod], outputs=output_inv)
    
    with gr.Tab("Обратный элемент"):
        with gr.Row():
            element = gr.Number(label="Элемент")
            mod = gr.Number(label="Модуль")
            output_inv = gr.Textbox(label="Обратный элемент", interactive=False)
        gr.Button("Вычислить").click(modular_inverse, inputs=[element, mod], outputs=output_inv)

    with gr.Tab("Линейное сравнение вида ax=b(mod m)"):
        with gr.Row():
            a = gr.Number(label="a")
            b = gr.Number(label="b")
            m = gr.Number(label="m")
            output_eq = gr.Textbox(label="Решения", interactive=False)
        gr.Button("Решить").click(solve_linear_congruence, inputs=[a, b, m], outputs=output_eq)

    with gr.Tab("Система сравнений"):
        with gr.Row():
            a = gr.Number(label="a")
            b = gr.Number(label="b")
            c = gr.Number(label="c")
            d = gr.Number(label="d")
            m = gr.Number(label='m')
            output_sys = gr.Textbox(label="Решения", interactive=False)
        gr.Button("Решить").click(system_lin_con, inputs=[a, b, c, d, m], outputs=output_sys)

    with gr.Tab("Частотный анализ"):
        text_input = gr.Textbox(label="Шифр-текст", lines=5)
        output_freq = gr.Textbox(label="Частота символов", interactive=False)
        gr.Button("Анализировать").click(frequency_analysis, inputs=text_input, outputs=output_freq)

    with gr.Tab("Дешифрование"):
        ciphertext = gr.Textbox(label="Зашифрованный текст", lines=5)
        output_dec = gr.Textbox(label="Дешифрованный текст", interactive=False)
        gr.Button("Дешифровать").click(affine_decryptor, inputs=ciphertext, outputs=output_dec)
app.launch()