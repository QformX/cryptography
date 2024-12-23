from math import isqrt

def binary_exponentiation(base, exp, mod):
    """
    Эффективный алгоритм быстрого возведения в степень по модулю.
    base^exp mod mod
    """
    result = 1                                  # Инициализируем результат как 1, так как любое число в степени 0 равно 1
    base = base % mod                           # Предварительно сокращаем основание по модулю для упрощения вычислений

    while exp > 0:                              # Пока показатель степени больше 0 
        if exp % 2 == 1:                        # Если текущий бит показателя степени нечётный
            result = (result * base) % mod      # Умножаем результат на текущее основание и берём по модулю
        base = (base * base) % mod              # Возводим основание в квадрат и берём по модулю
        exp = exp // 2                          # Делим показатель степени на 2 (сдвигаем биты вправо)
    return result

def baby_step_giant_step(a, b, p):
    answers = []  # Хранение найденных решений
    indices = []  # Хранение индексов i и j, из которых вычислено решение
    message = ""

    # Вычисляем k = ⌊√p⌋ + 1
    k = isqrt(p) + 1
    message += f"Вычислено k = ⌊√{p}⌋ + 1 = {k}\n"

    # Построение последовательности y_n = a^(n*k) mod p
    value = {}  # Для быстрого поиска совпадений
    for i in range(1, k + 1):
        y_n = binary_exponentiation(a, i * k, p)
        value[y_n] = i # записываем результат и итерацию (результат: итерация)
        message += f"y_{i} = {a}^({i}*{k}) mod {p} = {y_n}\n"

    # Построение последовательности z_n = b * a^n mod p и поиск совпадений
    for j in range(k):
        z_n = (binary_exponentiation(a, j, p) * b) % p
        message += f"z_{j} = {b} * {a}^{j} mod {p} = {z_n}\n"

        # Проверяем, есть ли совпадение между y_n и z_n
        if z_n in value:
            i = value[z_n]  # Получаем индекс i из y_n
            x = i * k - j  # Вычисляем x
            message += f"Совпадение найдено: y_{i} = z_{j} = {z_n}\n"
            message += f"Вычислено x = {i} * {k} - {j} = {x}\n"

            if x < p:
                answers.append(x)  # Сохраняем решение
                indices.append((i, j))  # Сохраняем индексы

    # Если решения найдены, возвращаем их, иначе выводим сообщение
    if answers:
        return answers, indices, message
    else:
        print("Решение не найдено.")
        return None