from sympy import isprime
import gradio as gr

alphabet = {
    'А': 10, 'Б': 11, 'В': 12, 'Г': 13, 'Д': 14, 'Е': 15, 'Ж': 16, 'З': 17, 'И': 18, 'Й': 19, 'К': 20,
    'Л': 21, 'М': 22, 'Н': 23, 'О': 24, 'П': 25, 'Р': 26, 'С': 27, 'Т': 28, 'У': 29, 'Ф': 30,
    'Х': 31, 'Ц': 32, 'Ч': 33, 'Ш': 34, 'Щ': 35, 'Ъ': 36, 'Ы': 37, 'Ь': 38, 'Э': 39, 'Ю': 40, 'Я': 41, ' ' : 99
}

alphabet_inverse = {
        10: 'А', 11: 'Б', 12: 'В', 13: 'Г', 14: 'Д', 15: 'Е',
        16: 'Ж', 17: 'З', 18: 'И', 19: 'Й', 20: 'К', 21: 'Л',
        22: 'М', 23: 'Н', 24: 'О', 25: 'П', 26: 'Р', 27: 'С',
        28: 'Т', 29: 'У', 30: 'Ф', 31: 'Х', 32: 'Ц', 33: 'Ч',
        34: 'Ш', 35: 'Щ', 36: 'Ъ', 37: 'Ы', 38: 'Ь', 39: 'Э',
        40: 'Ю', 41: 'Я', 99: ' '
    }

def preprocess_text(text):
    code = ""
    russian_alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    text = ''.join(c for c in text if c in russian_alphabet)
    text = text.upper()
    for item in text:
        print(item)
        code += (str(alphabet[item]))
    return code

def divide_n(code, n):
    blocks = []
    current_block = ""
    for item in code:
        current_block += item
        if (int(current_block) > n):
            if int(item) == 0:
                last_value = current_block[-2:]
                current_block = current_block[:-2]
                blocks.append(current_block)
                current_block = last_value
            else:  
                current_block = current_block[:-1]
                blocks.append(current_block)
                current_block = item
    
    blocks.append(current_block)
    
    return blocks

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e, phi_n):
    gcd, x, _ = extended_gcd(e, phi_n)
    if gcd != 1:
        raise Exception("Европейский алгоритм не работает для заданных e и phi_n")
    else:
        return x % phi_n

def generate_keypair(p, q):
    """Генерация пары ключей RSA"""
    n = p * q
    phi_n = (p - 1) * (q - 1)
    key_pairs = []
    e = 17
    
    while len(key_pairs) < 3:
        if isprime(e):
            print(e)
            if phi_n % e != 0 and extended_gcd(e, phi_n)[0] == 1:
                d = mod_inverse(e, phi_n)
                key_pairs.append(((e, n), (d, n)))
        e += 2

    return key_pairs

def generate_keypair_with(p, q, e):
    n = p * q
    phi_n = (p - 1) * (q - 1)
    if phi_n % e != 0 and extended_gcd(e, phi_n)[0] == 1:
        d = mod_inverse(e, phi_n)
    else:
        raise gr.Error('Error: e must be coprime to phi(n) and non-zero.')
    
    return ((e, n),(d, n))

def encrypt(message, public_key):
    """Шифрование сообщения с использованием открытого ключа"""
    e, n = public_key
    ciphertext_int = []
    decrypted_str = ""
    for block in message:
        block = int(block)
        ciphertext_int.append(pow(block, e, n))
        
    #for block in ciphertext_int:
    #    decrypted_str += str(block)
        
    #result = ''
    
    #for i in range(0, len(decrypted_str), 2):
    #    num_str = decrypted_str[i:i+2]
    #    number = int(num_str)
        
    #    if number in alphabet_inverse:
    #        result += alphabet_inverse[number]
    
    return ciphertext_int

def decrypt(ciphertext, private_key):
    """Расшифровка сообщения с использованием закрытого ключа"""
    d, n = private_key
    decrypted_int = []
    decrypted_str = ""
    for block in ciphertext:
        decrypted_int.append(pow(block, d, n))
        
    for block in decrypted_int:
        decrypted_str += str(block)
        
    result = ''
    
    for i in range(0, len(decrypted_str), 2):
        num_str = decrypted_str[i:i+2]
        number = int(num_str)
        
        if number in alphabet_inverse:
            result += alphabet_inverse[number]

    return result
            
    