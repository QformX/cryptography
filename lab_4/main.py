from utils import *
import gradio as gr

n = 1

def decrypt_interface(d, n, ciphertext_str):
    private_key = (d, n)
    ciphertext = list(map(int, ciphertext_str.strip("[]").split(", ")))
    print(ciphertext)
    return decrypt(ciphertext, private_key)

def keys_interface(p, q):
    key_pairs = generate_keypair(p, q)
    global n
    n = p*q
    
    formatted_keys = []

    for public_key, private_key in key_pairs:
        e, n = public_key
        d, _ = private_key  # Второе значение n не нужно, так как оно одинаково
        formatted_keys.append(f"e = {e}, n = {n}\nd = {d}, n = {n}")

    result = "\n\n".join(formatted_keys)
    
    return result

def encrypt_interface(e, d, text):
    preprocessed_text = preprocess_text(text)
    code_blocks = divide_n(preprocessed_text, n)
    public_key = (e, d)
    
    return encrypt(code_blocks, public_key)

        

with gr.Blocks() as demo:
    gr.Markdown("### RSA Encryption and Decryption")
    with gr.Row():
        with gr.Column():
            with gr.Row():
                p_input = gr.Number(label="Enter prime number p")
                q_input = gr.Number(label="Enter prime number q")
            generate_button = gr.Button("Generate Keys and Encrypt Message")
        
            output = gr.Textbox(label="Output")

        generate_button.click(keys_interface, inputs=[p_input, q_input], outputs=output)
        
        with gr.Column():
            with gr.Row():
                e_input = gr.Number(label="e для открытого ключа")
                n_input = gr.Number(label="n открытого ключа")
                text = gr.Textbox(label="Исходный текст")
            
            encrypt_button = gr.Button("Зашифровать текст")
            output_encrypt = gr.Textbox(label="Output")
            
            encrypt_button.click(encrypt_interface, inputs=[e_input, n_input, text], outputs=output_encrypt)
            
        with gr.Column():
            with gr.Row():
                d_input = gr.Number(label="d для открытого ключа")
                n_input = gr.Number(label="n открытого ключа")
                code_blocks = gr.Textbox(label="Список значений блоков")
            
            decrypt_button = gr.Button("Расшифровать текст")
            output_decrypt = gr.Textbox(label="Output")
            
            decrypt_button.click(decrypt_interface, inputs=[d_input, n_input, code_blocks], outputs=output_decrypt)

demo.launch()
