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

def cesar_decipher(text):
    syms = [sym for sym in text]
    for i in range(32):
        a = []
        out = ''
        for j in range(len(syms)):
            a.append(dict_reverse[min_in_ring(dict[syms[j]], i, 32)])
        for h in range(len(a)):
            out += a[h]
        print(f'{out}, {i}')
    return 0

def cesar_decipher_with_key(text, key):
    syms = [sym for sym in text]
    a = []
    out = ''
    for j in range(len(syms)):
        a.append(dict_reverse[min_in_ring(dict[syms[j]], key, 32)])
    for h in range(len(a)):
        out += a[h]
    print(f'{out}')
    return 0

def cesar_encrypt(text, key):
    syms = [sym for sym in text]
    a = []
    out = ''
    for j in range(len(syms)):
        a.append(dict_reverse[add_in_ring(dict[syms[j]], key, 32)])
    for h in range(len(a)):
        out += a[h]
    print(f'{out}')
    return out

cesar_decipher('шйльфавкж')
key = int(input())
text = input()
out = cesar_encrypt(text, key)
cesar_decipher_with_key(out, key)