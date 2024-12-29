from utils import gcd_extended

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
