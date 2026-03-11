#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

df = pd.read_csv('data/divisas.csv')

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Tasas de Cambio vs USD', fontsize=16, fontweight='bold')

# Gráfica 1: Tasas de cambio (barras)
ax1 = axes[0]
ax1.bar(df['moneda_destino'], df['tasa_cambio'], color='#4ecdc4')
ax1.set_title('Tasa de Cambio (1 USD = X moneda)')
ax1.set_ylabel('Tasa')
ax1.tick_params(axis='x', rotation=45)
ax1.grid(axis='y', alpha=0.3)

# Gráfica 2: Valor inverso (cuántos USD vale 1 unidad de cada moneda)
ax2 = axes[1]
ax2.bar(df['moneda_destino'], df['inversa'], color='#ff6b6b')
ax2.set_title('Valor en USD de cada moneda (inversa)')
ax2.set_ylabel('USD')
ax2.tick_params(axis='x', rotation=45)
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('data/divisas_analysis.png', dpi=300, bbox_inches='tight')
print("✅ Gráfica guardada en data/divisas_analysis.png")
plt.show()