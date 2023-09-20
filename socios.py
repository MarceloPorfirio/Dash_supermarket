import pandas as pd

# Carregue o DataFrame (substitua "data.csv" pelo nome do seu arquivo CSV)
data = pd.read_csv("supermarket_sales - Sheet1.csv")

# Converta a coluna 'Date' para o tipo datetime, se necessário
data['Date'] = pd.to_datetime(data['Date'])

# Encontre a menor data
min_date = data['Date'].min()

# Encontre a maior data
max_date = data['Date'].max()

print(f"Menor Data: {min_date}")
print(f"Maior Data: {max_date}")
