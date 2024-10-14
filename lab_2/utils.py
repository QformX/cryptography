from math import gcd
from collections import Counter

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# Функция для нахождения обратного элемента
def modular_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"No modular inverse for {a} mod {m}")
    return x % m

# Функция для решения сравнения ax ≡ b mod m
def solve_linear_congruence(a, b, m):
    g = gcd(a, m)
    if b % g != 0:
        return "Нет решения"
    a //= g
    b //= g
    m //= g
    x0 = modular_inverse(a, m)
    if x0 is None:
        return "Нет обратного элемента"
    solutions = [(x0 + i * (m)) % (m * g) for i in range(g)]
    return solutions

def solve_system(a, b, c, d, m):
    # Приводим систему к x
    coeff = (a - c) % m
    rhs = (d - b) % m

    # Находим обратный элемент
    inv_coeff = modular_inverse(coeff, m) if coeff != 0 else None
    
    if coeff == 0:
        if rhs == 0:
            return "Бесконечное количество решений"
        else:
            return "Нет решений"

    x = (rhs * inv_coeff) % m
    y = (b - a * x) % m

    return x, y

# Функция для частотного анализа шифр-текста
def frequency_analysis(text):
    text = text.lower()
    frequency = Counter(text)
    most_common = frequency.most_common(2)
    return most_common

# Функция для дешифрования текста по аффинному шифру
def decrypt_affine(ciphertext, a, b, m):
    try:
        inv_a = modular_inverse(a, m)
        if inv_a is None:
            return "Модуль не обратим"
        plaintext = ""
        for char in ciphertext:
            if char.isalpha():
                x = (inv_a * (ord(char.lower()) - ord('a') - b)) % 26
                plaintext += chr(x + ord('a'))
            else:
                plaintext += char
        return plaintext
    except Exception as e:
        return str(e)