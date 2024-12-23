from math import isqrt

primes_list = []
blocks_list = []

def gcd_extended(a, b):
    """Расширенный алгоритм Евклида для нахождения НОД и коэффициентов x и y."""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e, n):
    """
    Нахождение обратного числа d к e по модулю n.
    """
    gcd, x, _ = gcd_extended(e, n)
    if gcd != 1:
        raise ValueError("Обратного числа не существует (e и n не взаимно простые).")
    return x % n

def modular_exponentiation(base, exp, mod):
    """Бинарный алгоритм возведения в степень. Вычисляет block ^ e mod n"""
    result = 1                                  # Инициализируем результат как 1, так как любое число в степени 0 равно 1
    base = base % mod                           # Предварительно сокращаем основание по модулю для упрощения вычислений

    while exp > 0:                              # Пока показатель степени больше 0 
        if exp % 2 == 1:                        # Если текущий бит показателя степени нечётный
            result = (result * base) % mod      # Умножаем результат на текущее основание и берём по модулю
        base = (base * base) % mod              # Возводим основание в квадрат и берём по модулю
        exp = exp // 2                          # Делим показатель степени на 2 (сдвигаем биты вправо)
    return result

def generate_primes(n):
    """Генератор простых чисел до n с помощью решета Эратосфена."""
    sieve = [False, False] + [True] * (isqrt(n) - 1)  # Сразу исключаем 0 и 1

    primes = []  # Список для хранения простых чисел
    for number in range(2, isqrt(n) + 1):
        if sieve[number]:
            primes.append(number)  # Добавляем простое число в список
            # Помечаем все кратные числа как составные
            for k in range(number * number, isqrt(n) + 1, number):
                sieve[k] = False

    return primes

def trial_division(n):
    """Проводит факторизацию числа n методом пробного деления"""
    # Создаем список простых чисел до n
    for prime in generate_primes(n):
        primes_list.append(prime)
    
    # Формируем блоки из простых чисел
    block_size = 3
    for i in range(0, len(primes_list), block_size):
        blocks_list.append(primes_list[i:i + block_size])
    
    factors = {}
    for block in blocks_list:
        if n == 1:  # Если n уже разложено полностью
            break

        # Произведение чисел в блоке
        group_product = 1
        for num in block:
            group_product *= num

        # НОД текущего числа и произведения группы
        gcd_value, _, _ = gcd_extended(n, group_product)

        if gcd_value > 1:  # Если найден общий делитель
            for prime in block:
                while n % prime == 0:  # Пока n делится на prime
                    factors[prime] = factors.get(prime, 0) + 1
                    n //= prime  # Обновляем n, деля на prime

    # Если после всех делений осталось число больше 1, добавляем его
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors

def calculate_private_key(e, p, q):
    """Вычисляет закрытый ключ d"""
    phi_n = (p - 1) * (q - 1)
    d = mod_inverse(e, phi_n)  # Используем модульное обратное
    return d

def decrypt_message(C, d, n):
    """Расшифровывает сообщение C с помощью d и n"""
    M = modular_exponentiation(C, d, n)
    return M

def process_message(e, n, C):
    # Факторизация n
    factors = trial_division(n)
    
    primes = []
    for item in factors.keys():
        primes.append(item)
    
    if len(primes) != 2:
        return "n должно быть произведением двух простых чисел."
    p, q = primes[0], primes[1]

    # Закрытый ключ
    d = calculate_private_key(e, p, q)

    # Расшифрование сообщения
    M = decrypt_message(C, d, n)

    return f"Простые числа: {primes_list}\nБлоки: {blocks_list}\nПринадлежности n: p = {p}, q = {q}\nЗакрытый ключ d = {d}\nРасшифрованное сообщение M = {M}"