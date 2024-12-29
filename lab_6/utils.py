import math

def sieve_factorization(m, a, b, c):
    """
    Факторизация числа методом квадратичного решета с наложением решет по модулям a, b, c.

    :param m: число для факторизации
    :param a: модуль решета A
    :param b: модуль решета B
    :param c: модуль решета C
    :return: кортеж найденных делителей или (None, None)
    """
    # Предварительная проверка на квадратность числа m
    if is_perfect_square(m):
        print(f"Число {m} является квадратом, факторизация не требуется.")
        root = integer_sqrt(m)
        print(f"Корень числа {m} = {root}")
        return root, root

    # Проверка, что каждая пара чисел из (a, b, c) взаимно просты
    if not (are_coprime(a, b) and are_coprime(a, c) and are_coprime(b, c)):
        print("Одно или несколько чисел a, b, c не являются взаимно простыми. Введите числа, которые попарно просты.")
        return None, None

    print("\n---- Метод квадратичного решета с наложением решет ----")

    start = integer_sqrt(m) + 1
    end = (m + 1) // 2
    print(f"Интервал чисел для наложения решет: от {start} до {end}")

    # Вспомогательная функция для вывода решет
    def print_sieve_table(x_values, mod, sieve_check):
        print(f"\nРешето для модуля {mod}:")

        # Заголовок таблицы
        header = f"{'x':<3}| " + "| ".join(f"{x:<3}" for x in x_values)

        # Разделительная линия
        line = "-" * len(header)

        # Строка x^2 mod p
        x_squared = f"{f'x^2 mod {mod}':<3}| " + " | ".join(f"{(x**2) % mod:<3}" for x in x_values)

        # Строка Z = x^2 - m mod p
        z_values = f"{f'Z = x^2 - m mod {mod}':<3} | " + "| ".join(f"{(x**2 - m) % mod:<3}" for x in x_values)

        # Строка результатов решета (z = (x^2 - m) mod mod; z^((p-1)/2) mod p = p - 1)
        sieve_result = f"{sieve_check:<3}| " + "| ".join(" X " if is_quadratic_nonresidue((x**2 - m) % mod, mod) else "   " for x in x_values)

        # Вывод таблицы
        print(header)
        print(line)
        print(x_squared)
        print(z_values)
        print(sieve_result)

    x_values_a = range(a)
    x_values_b = range(b)
    x_values_c = range(c)

    print_sieve_table(x_values_a, a, "S_" + str(a))
    print_sieve_table(x_values_b, b, "S_" + str(b))
    print_sieve_table(x_values_c, c, "S_" + str(c))

    # Проход по интервалу для проверки
    for step, x in enumerate(range(start, end), 1):
        x2 = x**2
        z = x2 - m

        print(f"\n{step}. : Проверяем x = {x}: x^2 = {x2}, z = x^2 - m = {z}")

        # Проверка условия наложения решет
        sieve_hit = False
        # (x - (isqrt(m) + 1) mod a == 2 mod a
        if (x - start) % a == 2 % a:
            print(f"S_{a} = {x % a} = X")
            sieve_hit = True
        if (x - start) % b == 1 % b:
            print(f"S_{b} = {x % b} = X")
            sieve_hit = True
        if (x - start) % c == 5 % c:
            print(f"S_{c} = {x % c} = X")
            sieve_hit = True

        if sieve_hit:
            print(f"Наложение решет найдено для x = {x}")

        # Сравнение для наложения
        print(f"Сравнение для x = {x}: S_{a} = {x % a}, S_{b} = {x % b}, S_{c} = {x % c}")

        # y = sqrt(z), или же если z = y^2, то m факторизуется как p*q
        sqrt_z = integer_sqrt(z)
        if sqrt_z * sqrt_z == z:
            y = sqrt_z
            print()
            print(f"Число Z = {z} оказалось полным квадратом, y = {y}")

            p = x + y
            q = x - y
            print(f"Найденные делители: p = {p}, q = {q}")

            if m % p == 0 and m % q == 0:
                print(f"На шаге {step} число {m} факторизуется как {p} * {q}")
                return p, q
        else:
            print('z != y^2, продолжаем перебор')
    print("Не удалось найти делители с использованием квадратичного решета.")
    return None, None

def f(x, m):
    """Циклическая функция для метода ρ"""
    return (x**2 - 1) % m

def rho_method(m, x0, y0):
    """
    Метод ρ для факторизации числа m.
    
    :param m: число для факторизации
    :param x0: начальное значение x
    :param y0: начальное значение y
    :return: найденный делитель или None
    """
    x1 = x0
    x2 = y0
    step = 0

    while True:
        step += 1
        x1 = f(x1, m)
        x2 = f(f(x2, m), m)

        a = abs(x1 - x2) # a = |x1 - x2|
        d = gcd_extended(a, m)[0] # НОД a, m

        print(f"Шаг {step}: x1 = {x1}, x2 = {x2}, a = |{x1} - {x2}| = {a}, d = НОД(a, m) = {d}")

        if 1 < d < m:
            print()
            print(f"На шаге {step} найден делитель: {d}")
            return d
        if step > 100:
            print("Превышен лимит шагов, делитель не найден.")
            return None

def gcd_extended(a, b):
    """Расширенный алгоритм Евклида для нахождения НОД и коэффициентов"""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def integer_sqrt(n):
    """Целочисленный квадратный корень"""
    x = n
    while True:
        y = (x + n // x) // 2
        if y < x:
            x = y
        else:
            break
    return int(x)

def is_perfect_square(m):
    """Проверка, является ли число m полным квадратом"""
    return int(math.isqrt(m)) ** 2 == m

def is_prime(n):
    """Проверка, является ли число простым"""
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def are_coprime(a, b):
    """Проверка, взаимно ли просты числа a и b"""
    return gcd_extended(a, b)[0] == 1

def modular_exponentiation(base, exponent, modulus):
    """Возведение в степень по модулю"""
    result = 1
    base = base % modulus
    while exponent > 0:
        if (exponent % 2) == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

def is_quadratic_nonresidue(z, p):
    """Проверка, является ли z квадратичным невычетом по модулю p"""
    return modular_exponentiation(z, (p - 1) // 2, p) == p - 1
