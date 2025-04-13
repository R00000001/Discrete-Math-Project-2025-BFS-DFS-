import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    # Створення директорії для збереження графіків, якщо вона не існує
    output_dir = "graphs"
    os.makedirs(output_dir, exist_ok=True)

    # Завантаження даних з TSV файлу
    try:
        df = pd.read_csv("results.tsv", sep="\t")
    except FileNotFoundError:
        print("Файл results.tsv не знайдено. Будь ласка, запустіть спочатку програму, яка генерує результати експериментів.")
        return

    # Для поліпшення вигляду графіків встановимо стиль seaborn
    sns.set(style="whitegrid")

    # Отримання унікальних методів та способів представлення графа
    methods = df["method"].unique()
    representations = df["representation"].unique()

    # Побудова графіків для кожної комбінації метод + представлення
    for method in methods:
        for rep in representations:
            # Фільтрування даних
            subset = df[(df["method"] == method) & (df["representation"] == rep)]
            # Перетворення часу з секунд у мілісекунди
            subset = subset.copy()
            subset["time_ms"] = subset["average_time_sec"] * 1000

            plt.figure(figsize=(10, 6))
            
            # Побудова лінійного графіку за допомогою Seaborn для кожного розміру графа
            sns.lineplot(
                data=subset,
                x="density",
                y="time_ms",
                hue="nodes",
                marker="o",
                palette="tab10"
            )

            plt.title(f"{method} ({rep})")
            plt.xlabel("Щільність (%)")
            plt.ylabel("Час виконання (мс)")
            plt.legend(title="Nodes")
            plt.tight_layout()

            # Збереження графіку
            filename = f"{method}_{rep}.png"
            filepath = os.path.join(output_dir, filename)
            plt.savefig(filepath)
            plt.close()
            print(f"Збережено графік: {filepath}")

if __name__ == "__main__":
    main()

