from blocks import *
import gradio as gr

def update_inputs_enc(selected_key):
    key = load_keys_from_json()
    if selected_key in key:
        e, d, n = key[selected_key]
        return e, n
    return None, None

def update_inputs_dec(selected_key):
    key = load_keys_from_json()
    if selected_key in key:
        e, d, n = key[selected_key]
        return d, n
    return None, None

def update_choices():
    return list(key_dict.keys())      

with gr.Blocks() as demo:
    gr.Markdown("### RSA Encryption and Decryption")
    with gr.Row():
        with gr.Column():
            with gr.Row():
                p_input = gr.Number(label="Enter prime number p")
                q_input = gr.Number(label="Enter prime number q")
                e_input = gr.Number(label="Enter prime number e")
            generate_button = gr.Button("Сгенерировать ключи")
        
            output = gr.Textbox(label="Output")
            clear_button = gr.Button("Очистить ключи")
            notification = gr.HTML("")

        generate_button.click(keys_interface, inputs=[p_input, q_input, e_input], outputs=output)
        clear_button.click(clear_keys_list)
        
        with gr.Column():
            key_dict = ["1 ключ", "2 ключ", "3 ключ"] # Изначально загружаем доступные ключи из JSON

            # Добавляем Dropdown для выбора ключей
            select_keys_enc = gr.Dropdown(
                label="Выберите ключи",
                choices=list(key_dict),  # Устанавливаем начальные значения из key_dict
                value=None,
            )

            with gr.Row():
                e_input = gr.Number(label="e для открытого ключа", interactive=False)
                n_input = gr.Number(label="n открытого ключа", interactive=False)
                text = gr.Textbox(label="Исходный текст")
            
            encrypt_button = gr.Button("Зашифровать текст")
            output_encrypt = gr.Textbox(label="Output")
            copy_button = gr.Button("Скопировать для дешифровки")
            

            # Обработчик изменения выбора в Dropdown
            select_keys_enc.change(
                update_inputs_enc, 
                inputs=select_keys_enc, 
                outputs=[e_input, n_input]
            )
            

            # Обработчик нажатия кнопки шифрования
            encrypt_button.click(encrypt_interface, inputs=[e_input, n_input, text], outputs=output_encrypt)
        
        with gr.Column():
            
            select_keys_dec = gr.Dropdown(
                label="Выберите ключи",
                choices=list(key_dict),  # Устанавливаем начальные значения из key_dict
                value=None,
            )
            
            with gr.Row():
                d_input = gr.Number(label="d для открытого ключа")
                n_input = gr.Number(label="n открытого ключа")
                code_blocks = gr.Textbox(label="Список значений блоков")
            
            decrypt_button = gr.Button("Расшифровать текст")
            output_decrypt = gr.Textbox(label="Output")
            
            select_keys_dec.change(
                update_inputs_dec, 
                inputs=select_keys_dec, 
                outputs=[d_input, n_input]
            )
            
            decrypt_button.click(decrypt_interface, inputs=[d_input, n_input, code_blocks], outputs=output_decrypt)

demo.launch()
