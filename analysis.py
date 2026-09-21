import pandas as pd
import matplotlib.pyplot as plt
import os

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
top_expensive = df.nsmallest(TOP_N, "price_num")[["title", "price_num", "link", "location", "condition"]]
for _, row in top_expensive.iterrows():
    print(f"{row['price_num']:>10,} ֏  {row['title'][:120]}")
    print(f"Ссылка на объявление: {row['link']} | Состояние: {row['condition']} | Локация: {row['location']}")
print()