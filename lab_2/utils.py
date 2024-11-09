from math import gcd
from collections import Counter
import heapq

alphabet = [
    'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з',
    'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п',
    'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч',
    'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я'
]

m_alphabet = len(alphabet)  # Размер алфавита (32)

char_to_num = {char: idx for idx, char in enumerate(alphabet)}
num_to_char = {idx: char for idx, char in enumerate(alphabet)}

freq_data = "аоенрислкдытмувпячгбйжцщшфъэьюё"

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# Функция для нахождения обратного элемента
def modular_inverse(a, m):
    div, u, v = extended_gcd(a, m)
    if div == 1:
        u = u % m
        return u
    return 0

# Функция для решения сравнения ax ≡ b mod m
def solve_linear_congruence(a, b, m):
    div, u, v = extended_gcd(a, m)
    if b%div != 0:
        print('Число ' + str(div) + ' не делит число ' + str(b) + ' => решений нет')
        return []
    x = [None] * div   
    ai = a/div
    bi = b/div
    mi = m/div
    x[0] = (bi * modular_inverse(ai, mi)) % m
    for i in range(1, div):
        x[i] = x[0] + i*mi
        while x[i] > m:
            x[i] -= m
    return [int(i) for i in x]

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

def system_lin_con(a, b, c, d, mod):
    a_sys = a - c
    b_sys = b - d
    if a_sys < 0:
        a_sys = -a_sys
        b_sys = -b_sys
    x1 = solve_linear_congruence(a_sys, b_sys, mod)
    y1 = []
    for i in range(len(x1)):
        y1.append((b - a*x1[i]) % mod)
    x2 = solve_linear_congruence(a_sys, -b_sys, mod)
    y2 = []
    for i in range(len(x2)):
        y2.append((b - c*x2[i]) % mod)
    x = x1 + x2
    y = y1 + y2
    return x, y

# Функция для частотного анализа шифр-текста
def frequency_analysis(sypher_text):
    fa = dict()
    for letter in char_to_num.keys():
        fa[letter] = round(sypher_text.count(letter)/len(sypher_text), 3)
    return fa

# Функция для дешифрования текста по аффинному шифру
def decrypt_affine(ciphertext, a_inv, b, m=m_alphabet, num_to_char_map=num_to_char, char_to_num_map=char_to_num):
    """Расшифровка афинного шифра для заданных a_inv и b."""
    decrypted = ''
    for char in ciphertext:
        if char.lower() in char_to_num_map:
            y = char_to_num_map[char.lower()]
            x = (a_inv * (y - b)) % m
            decrypted_char = num_to_char_map[x]
            # Сохраняем регистр исходного символа
            if char.isupper():
                decrypted += decrypted_char.upper()
            else:
                decrypted += decrypted_char
        else:
            # Если символ не в алфавите, оставляем его без изменений
            decrypted += char
    return decrypted

def Hypotesis(hypo, f1, f2):
    print('Гипотеза: \n' +
        ' Ek(' + f1 + ') = ' + hypo[0] + ', Ek(' + f2 + ') = ' + hypo[1] + '\n' +
        ' или \n' +
        ' Ek(' + f1 + ') = ' + hypo[1] + ', Ek(' + f2 + ') = ' + hypo[0])

def affine_decryptor(ciphertext):
    F = 'оеаитнсрвлкмдпуяызъбгчйхжюшцщэф'
    fa = frequency_analysis(ciphertext)
    hypo = list(heapq.nlargest(2, fa, key=fa.get))
    
    flag = 1
    for i in range(len(F)):
        if flag == 0:
            break
            
        for j in range(i+1, len(F)-i):
            if flag == 0:
                break
            Hypotesis(hypo, F[i], F[j])
            a, b = system_lin_con(char_to_num[F[i]], char_to_num[hypo[0]], char_to_num[F[j]], char_to_num[hypo[1]], 32)
    
            with open('decrypted_messages.txt', 'w', encoding='utf-8') as file:
                for i in range(len(a)):
                    if flag == 0:
                        break
                    if modular_inverse(a[i], 32) == 0:
                        print('Ключ ' + str(a[i]) + '-' + str(b[i]) + ' не подходит, тк. обратного элемента к ' + str(a[i]) + ' в кольце вычетов по mod 32 не существует')
                    else:
                        open_text = []
                        for letter in ciphertext:
                            open_text.append( num_to_char[(modular_inverse(a[i], 32) * (char_to_num[letter] - b[i])) % 32] )
                        print('Ключ: ' + str(a[i]) + '-' + str(b[i]))
                        print('Открытый текст: ' + ''.join(open_text))

    print("Расшифровка завершена. Результаты сохранены в 'decrypted_messages.txt'.")
    #return ans