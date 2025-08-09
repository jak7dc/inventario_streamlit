import pandas as pd

df = pd.read_excel('datos.xlsx', sheet_name='inventario_productos')

print(df.head())
print(df.describe())
print(df.info())
print(df.columns)

