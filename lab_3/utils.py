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
        return 0
    entropy = -sum((count / n) * math.log2(count / n) for count in frequency.values())
    
    return entropy / k

def plot_entropy(text):
    k_values = range(1, 6)
    entropy_values = [k_grams_frequency(text, k) for k in k_values]
    
    plt.figure(figsize=(10, 6))
    plt.plot(k_values, entropy_values, marker='o')
    plt.title('Зависимость Hk(T)/k от k')
    plt.xlabel('k')
    plt.ylabel('Hk(T)/k')
    plt.xticks(k_values)
    plt.grid()
    
    plt.savefig('entropy_plot.png')
    plt.close()

    return 'entropy_plot.png', list(entropy_values)

def main(text):
    plot_file, entropy_values = plot_entropy(text)
    return plot_file, entropy_values