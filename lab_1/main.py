dict = {
    'а':0,
    'б' : 1,
    'в' : 2,
    'г' : 3,
    'д' : 4,
    'е' : 5,
    'ж' : 6,
    'з' : 7,
    'и' : 8,
    'й' : 9,
    'к' : 10,
    'л' : 11,
    'м' : 12,
    'н' : 13,
    'о' : 14,
    'п' : 15,
    'р' : 16,
    'с' : 17,
    'т' : 18,
    'у' : 19,
    'ф' : 20,
    'х' : 21,
    'ц' : 22,
    'ч' : 23,
    'ш' : 24,
    'щ' : 25,
    'ъ' : 26,
    'ы' : 27,
    'ь' : 28,
    'э' : 29,
    'ю' : 30,
    'я' : 31,
}

dict_reverse = {
    0:'a',
    1:'б',
    2:'в',
    3:'г',
    4:'д',
    5:'е',
    6:'ж',
    7:'з',
    8:'и',
    9:'й',
    10:'к',
    11:'л',
    12:'м',
    13:'н',
    14:'о',
    15:'п',
    16:'р',
    17:'с',
    18:'т',
    19:'у',
    20:'ф',
    21:'х',
    22:'ц',
    23:'ч',
    24:'ш',
    25:'щ',
    26:'ъ',
    27:'ы',
    28:'ь',
    29:'э',
    30:'ю',
    31:'я'
}

def add_in_ring(a, b, n):
    """
    Складывает два числа a и b в кольце вычетов по модулю n.
    
    :param a: Первое число
    :param b: Второе число
    :param n: Модуль (размер кольца)
    :return: Сумма по модулю n
    """
    return (a + b) % n

def min_in_ring(a, b, n):
    """
    Складывает два числа a и b в кольце вычетов по модулю n.
    
    :param a: Первое число
    :param b: Второе число
    :param n: Модуль (размер кольца)
    :return: Сумма по модулю n
    """
    return (a - b) % n

def is_russian_letter(char):
    return 'а' <= char <= 'я' or 'А' <= char <= 'Я'

def cesar_decipher(text):
    syms = [sym for sym in text]
    b = ""
    for i in range(32):
        a = []
        out = ''
        for j in range(len(syms)):
            if is_russian_letter(syms[j]):
                a.append(dict_reverse[min_in_ring(dict[syms[j]], i, 32)])
            else:
                a.append(syms[j])
        for h in range(len(a)):
            out += a[h]
        b += f"k = {i}: {out}\n"
        print(f'k = {i}: {out}')
    return b

def cesar_decipher_with_key(text, key):
    syms = [sym for sym in text]
    a = []
    out = ''
    for j in range(len(syms)):
        if is_russian_letter(syms[j]):
            a.append(dict_reverse[min_in_ring(dict[syms[j]], key, 32)])
        else:
            a.append(syms[j])
    for h in range(len(a)):
        out += a[h]
    print(f'{out}')
    return out

def cesar_encrypt(text, key):
    syms = [sym for sym in text]
    a = []
    out = ''
    for j in range(len(syms)):
        if is_russian_letter(syms[j]):
            a.append(dict_reverse[add_in_ring(dict[syms[j]], key, 32)])
        else:
            a.append(syms[j])
    for h in range(len(a)):
        out += a[h]
    print(f'{out}')
    return out

def main_menu():
    while True:
        print("Выберите опцию:")
        print("1: Дешифровать текст с перебором ключа")
        print("2: Дешифровать текст с заданным ключом")
        print("3: Зашифровать текст с заданным ключом")
        print("4: Выход")

        choice = input("Введите номер опции: ")

        if choice == '1':
            text = input("Введите текст для дешифровки: ")
            cd = cesar_decipher(text)
            with open('output_many.txt', 'w', encoding='utf-8') as file:
                file.write(cd + '\n')

        elif choice == '2':
            text = input("Введите текст для дешифровки: ")
            key = int(input("Введите ключ: "))
            cesar_decipher_with_key(text, key)

        elif choice == '3':
            text = input("Введите текст для шифровки: ")
            key = int(input("Введите ключ: "))
            ce = cesar_encrypt(text, key)
            with open('output_one.txt', 'w', encoding='utf-8') as file:
                file.write(ce + '\n')

        elif choice == '4':
            print("Выход из программы.")
            break

        else:
            print("Неверный ввод. Пожалуйста, попробуйте снова.")

main_menu()