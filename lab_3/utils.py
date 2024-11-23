from collections import Counter
import math
import matplotlib.pyplot as plt

def preprocess_text(text):
    russian_alphabet = 'абвгдежзийклмнопрстуфхцчшщыэюя'
    text = text.lower()
    text = ''.join(c for c in text if c in russian_alphabet)
    return text

def k_grams_frequency(text, k):
    processed_text = preprocess_text(text)
    k_grams = [processed_text[i:i+k] for i in range(len(processed_text) - k + 1)]
    frequency = Counter(k_grams)
    
    n = sum(frequency.values())
    if n == 0:
        return 0, 0
    
    entropy = -sum((count / n) * math.log2(count / n) for count in frequency.values())
    
    return entropy, entropy / k

def plot_entropy(text):
    k_values = range(1, 6)
    entropy_values = []
    weighted_entropy_values = []

    for k in k_values:
        entropy, weighted_entropy = k_grams_frequency(text, k)
        entropy_values.append(entropy)
        weighted_entropy_values.append(weighted_entropy)

    entropy_k_10000, weighted_entropy_k_10000 = k_grams_frequency(text, 20)
    
    entropy_values.append(entropy_k_10000)
    weighted_entropy_values.append(weighted_entropy_k_10000)

    plt.figure(figsize=(10, 6))
    plt.plot(k_values, weighted_entropy_values[:-1], marker='o', label='Hk(T)/k для k=1 до 5')
    plt.axhline(y=weighted_entropy_k_10000, color='r', linestyle='--', label='Hk(T)/k для k=20')
    plt.title('Зависимость Hk(T)/k от k')
    plt.xlabel('k')
    plt.ylabel('Hk(T)/k')
    plt.xticks(k_values)
    plt.grid()
    plt.legend()
    
    plt.savefig('entropy_plot.png')
    plt.close()

    return 'entropy_plot.png', entropy_values, weighted_entropy_values

def main(text):
    plot_file, entropy_values, weighted_entropy_values = plot_entropy(text)
    return plot_file, entropy_values, weighted_entropy_values, weighted_entropy_values[-1]