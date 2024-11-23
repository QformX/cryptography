from utils import *
import gradio as gr

n = 1
formatted_keys = []

def decrypt_interface(d, n, ciphertext_str):
    private_key = (d, n)
    ciphertext = list(map(int, ciphertext_str.strip("[]").split(", ")))
    print(ciphertext)
    return decrypt(ciphertext, private_key)

def keys_interface(p, q, e):
    global formatted_keys
    formatted_keys.clear()  # Clear previous keys

    gr.Info("Starting the key generation process.")  # Informing user about the process start

    if p is None or q is None:
        raise gr.Warning("One or more input values are empty. Please enter valid prime numbers.")  # Warning for empty inputs

    try:
        n = p * q
        if e != 0:
            public_key, private_key = generate_keypair_with(p, q, e)
            e, n = public_key
            d, _ = private_key
            formatted_keys.append(f"e = {e}, n = {n}\nd = {d}, n = {n}")
            gr.Info("Keys successfully generated!")  # Info on successful generation
        else:
            key_pairs = generate_keypair(p, q)

            for public_key, private_key in key_pairs:
                e, n = public_key
                d, _ = private_key  # Второе значение n не нужно, так как оно одинаково
                formatted_keys.append(f"e = {e}, n = {n}\nd = {d}, n = {n}")

        return "\n\n".join(formatted_keys)

    except Exception as ex:
        raise gr.Error(f"An error occurred: {str(ex)}")

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
                e_input = gr.Number(label="Enter prime number e")
            generate_button = gr.Button("Generate Keys and Encrypt Message")
        
            output = gr.Textbox(label="Output")
            notification = gr.HTML("")

        generate_button.click(keys_interface, inputs=[p_input, q_input, e_input], outputs=output)
        
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
