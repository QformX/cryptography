from utils import *

n = 1
formatted_keys = []

def decrypt_interface(d, n, ciphertext_str):
    private_key = (d, n)
    ciphertext = list(map(int, ciphertext_str.strip("[]").split(", ")))
    return decrypt(ciphertext, private_key)

def keys_interface(p, q, e):
    global formatted_keys

    gr.Info("Starting the key generation process.")

    if p is None or q is None:
        raise gr.Warning("One or more input values are empty. Please enter valid prime numbers.")

    try:
        n = p * q
        if e != 0:
            public_key, private_key = generate_keypair_with(p, q, e)
            e, n = public_key
            d, _ = private_key
            formatted_keys.append((public_key, private_key))
            gr.Info("Keys successfully generated!")
        else:
            key_pairs = generate_keypair(p, q)
            for public_key, private_key in key_pairs:
                formatted_keys.append((public_key, private_key))

            gr.Info("Keys successfully generated!")

        # Сохранение ключей в JSON файл
        save_keys_to_json(formatted_keys)

        return "\n\n".join([f"e = {e}, n = {n}\nd = {d}, n = {n}" for public_key, private_key in formatted_keys 
                             for e, n in [public_key] 
                             for d in [private_key[0]]])

    except Exception as ex:
        raise gr.Error(f"An error occurred: {str(ex)}")

def encrypt_interface(e, n, text):
    preprocessed_text = preprocess_text(text)
    code_blocks = divide_n(preprocessed_text, n)
    public_key = (e, n)
    
    return encrypt(code_blocks, public_key)

def clear_keys_list():
    global formatted_keys
    formatted_keys.clear()
    
    with open("keys.json", "w") as json_file:
        json_file.write("")