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
    a =  a % m
    div, u, v = extended_gcd(a, m)
    if div != 1:
        return 0
    else:
        return u % m

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

def print_beautiful_output(x, y):
    print("Решения системы линейных конгруэнций:")
    print("{:<10} {:<10}".format("x", "y"))
    print("-" * 20)
    for x_val, y_val in zip(x, y):
        print("{:<10} {:<10}".format(x_val, y_val))

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
    print_beautiful_output(x, y)
    return x, y

def frequency_analysis(sypher_text):
    fa = dict()
    for letter in char_to_num.keys():
        fa[letter] = round(sypher_text.count(letter) / len(sypher_text), 3)
    # Сортируем словарь по значениям
    sorted_fa = dict(sorted(fa.items(), key=lambda item: item[1], reverse=True))
    return sorted_fa

def affine_decryptor(ciphertext):
    F = 'оеаитнсрвлкмдпуяызъбгчйхжюшцщэф'
    fa = frequency_analysis(ciphertext)
    hypo = list(heapq.nlargest(2, fa, key=fa.get))
    
    result = []
    flag = 1
    with open('decrypted_messages.txt', 'a', encoding='utf-8') as file:
        for i in range(len(F)):
            if flag == 0:
                break
                
            for j in range(i + 1, len(F) - i):
                if flag == 0:
                    break
                a, b = system_lin_con(char_to_num[F[i]], char_to_num[hypo[0]], char_to_num[F[j]], char_to_num[hypo[1]], 32)
    
                for k in range(len(a)):
                    if flag == 0:
                        break
                    if modular_inverse(a[k], 32) == 0:
                        message = f'Ключ {a[k]}-{b[k]} не подходит, тк. обратного элемента к {a[k]} в кольце вычетов по mod 32 не существует\n'
                        print(message)
                        file.write(message)
                        result.append(message)
                    else:
                        open_text = []
                        for letter in ciphertext:
                            inverse = int(modular_inverse(a[k], 32))
                            print(type(inverse))
                            num_value = char_to_num[letter] - b[k]
                            print(type(num_value))
                            index = (inverse * num_value) % 32
                            open_text.append(num_to_char[index])
                        message = f'Ключ: {a[k]}-{b[k]}\nОткрытый текст: {"".join(open_text)}\n'
                        print(message)
                        file.write(message)
                        result.append(message)

    result_message = "Расшифровка завершена. Результаты сохранены в 'decrypted_messages.txt'.\n" + ''.join(result)
    return result_message

