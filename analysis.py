import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import FuncFormatter

# Настройки
INPUT = "list.csv"
CHARTS_DIR = "charts"
TOP_N = 10

os.makedirs(CHARTS_DIR, exist_ok=True)

# Курсы валютной конвертации (актуально на 21.09.2026)
USD_TO_AMD = 363.44
EUR_TO_AMD = 417.05
RUB_TO_AMD = 4.31

# Функция перевода числа из строкового типа в целочисленный
def parse_price(value):
    if pd.isna(value):
        return None
    digits = ''.join(filter(str.isdigit, value))
    if not digits:
        return None
    number = int(digits)
    if "$" in value:
        return number * USD_TO_AMD
    if "€" in value:
        return number * EUR_TO_AMD
    if "₽" in value:
        return number * RUB_TO_AMD
    return number

# Читаем наш csv файл
df = pd.read_csv(INPUT, delimiter=';')
print(f"Загружено записей {len(df)}")
print(f"Колонки: {list(df.columns)}\n")

# Приводим колонку с ценами к типу int отбрасывая символы валюты
df["price_num"] = df["price"].apply(parse_price)
df = df.dropna(subset=["price_num"])
df["price_num"] = df["price_num"].astype(int)

# Вывод основных статистик
print("📊 ОБЩАЯ СТАТИСТИКА")
print(f"Всего объявлений:     {len(df)}")
print(f"Средняя цена:         {int(df['price_num'].mean()):,} ֏")
print(f"Медианная цена:       {int(df['price_num'].median()):,} ֏")
print(f"Минимальная цена:     {int(df['price_num'].min()):,} ֏")
print(f"Максимальная цена:    {int(df['price_num'].max()):,} ֏\n")

print(f"📊 ТОП {TOP_N} САМЫХ ДОРОГИХ ОБЪЯВЛЕНИЙ")
top_expensive = df.nlargest(TOP_N, "price_num")[["title", "price_num", "link", "location", "condition"]]
for _, row in top_expensive.iterrows():
    print(f"{row['price_num']:>10,} ֏  {row['title'][:120]}")
    print(f"Ссылка на объявление: {row['link']} | Состояние: {row['condition']} | Локация: {row['location']}")
print()

print(f"📊 ТОП {TOP_N} САМЫХ ДЕШЁВЫХ ОБЪЯВЛЕНИЙ")
top_cheapest = df.nsmallest(TOP_N, "price_num")[["title", "price_num", "link", "location", "condition"]]
for _, row in top_cheapest.iterrows():
    print(f"{row['price_num']:>10,} ֏  {row['title'][:120]}")
    print(f"Ссылка на объявление: {row['link']} | Состояние: {row['condition']} | Локация: {row['location']}")
print()

print("📊 РАСПРЕДЕЛЕНИЕ ПО ЛОКАЦИЯМ")
location_counts = df["location"].value_counts()
for loc, count in location_counts.items():
    print(f"{loc:<30} {count}")
print()

print("📊 РАСПРЕДЕЛЕНИЕ ПО СОСТОЯНИЮ")
condition_counts = df["condition"].value_counts()
for cond, count in condition_counts.items():
    print(f"{cond:<30} {count}")
print()

# График - Гистограмма цен
plt.figure(figsize=(10, 6))
plt.hist(df["price_num"], bins=30, color="blue", edgecolor="black")
plt.title("Распределение цен на видеокарты")
plt.xlabel("Цена (драм)")
plt.ylabel("Количество объявлений")
plt.grid(axis="y", alpha=0.3)
plt.gca().xaxis.set_major_formatter(
    FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", " ")))
plt.tight_layout()
plt.savefig(f"{CHARTS_DIR}/price_hist.png", dpi=100)
plt.close()
print(f"Файл {CHARTS_DIR}/price_hist.png успешно сохранён")

# График - Диаграмма распределения цен по ценовым категориям
bins = [0, 100_000, 250_000, 500_000, float("inf")]
labels = ["до 100k", "100k–250k", "250k–500k", "500k+"]
df["price_range"] = pd.cut(df["price_num"], bins=bins, labels=labels, right=False)
range_counts = df["price_range"].value_counts().reindex(labels)
plt.figure(figsize=(10, 6))
plt.bar(range_counts.index, range_counts.values, color="blue", edgecolor="black")
plt.title("Распределение видеокарт по ценовым категориям")
plt.xlabel("Цена (драм)")
plt.ylabel("Количество объявлений")
plt.grid(axis="y", alpha=0.3)
for i, v in enumerate(range_counts.values):
    plt.text(i, v + 2, str(v), ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig(f"{CHARTS_DIR}/price_ranges.png", dpi=100)
plt.close()
print(f"Файл {CHARTS_DIR}/price_ranges.png успешно сохранён")

# График - секторная диаграмма состояния видеокарты Новое/Использованное
plt.figure(figsize=(8, 8))
plt.pie(
    condition_counts.values,
    labels=condition_counts.index,
    autopct="%1.1f%%",
    colors=["green", "orange"],
    startangle=90,
    textprops={"fontsize": 12},
)
plt.title("Распределение видеокарт по состоянию", fontsize=14)
plt.tight_layout()
plt.savefig(f"{CHARTS_DIR}/condition_pie.png", dpi=100)
plt.close()
print(f"Файл {CHARTS_DIR}/condition_pie.png успешно сохранён")