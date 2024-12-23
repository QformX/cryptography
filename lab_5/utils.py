def trial_division(n):
    """Проводит факторизацию числа n методом пробного деления"""
    factors = []
    for i in range(2, int(n**0.5) + 1):
        while n % i == 0:
            factors.append(i)
            n //= i
    if n > 1:
        factors.append(n)
    return factors

def calculate_private_key(e, p, q):
    """Вычисляет закрытый ключ d"""
    phi_n = (p - 1) * (q - 1)
    d = pow(e, -1, phi_n)  # Используем модульное обратное
    return d

def decrypt_message(C, d, n):
    """Расшифровывает сообщение C с помощью d и n"""
    M = pow(C, d, n)
    return M

def process_message(e, n, C):
    # Факторизация n
    factors = trial_division(n)
    if len(factors) != 2:
        return "n должно быть произведением двух простых чисел."
    p, q = factors[0], factors[1]

    # Закрытый ключ
    d = calculate_private_key(e, p, q)

    # Расшифрование сообщения
    M = decrypt_message(C, d, n)

    return f"Принадлежности n: p = {p}, q = {q}\nЗакрытый ключ d = {d}\nРасшифрованное сообщение M = {M}"