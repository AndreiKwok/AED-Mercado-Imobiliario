import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


class Plotting():
    def __init__(self):
        pass

    def plot_Outliers(self, country: pd.DataFrame, median_rental_price: float) -> None:
        plt.figure(figsize=(12, 6))

        # Plotar os dados do Rent Index
        plt.scatter(country["Country"], country["Rent Index"], 
                label='Outliers', 
                color='blue', 
                alpha=0.7,
                linewidth=1)

        # Linha da mediana
        plt.axhline(y=median_rental_price, 
                    color='red', 
                    linestyle='--', 
                    linewidth=2,
                    label=f'Mediana (USD {median_rental_price:.4f})')

        # Ajustes do gráfico
        plt.title('Ouliers vs. Mediana', fontsize=14)
        plt.xlabel('Amostras', fontsize=12)
        plt.ylabel('Valor (USD)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.tight_layout()

        plt.show()
        
    def plot_graphic_dispersion(self, df: pd.DataFrame, limite_inferior: float, limite_superior: float) -> None:
        # Criar coluna de outliers
        df["Outlier"] = (df["Rent Index"] < limite_inferior) | (df["Rent Index"] > limite_superior)
        # Plotar
        plt.figure(figsize=(12, 7))
        sns.set_style("whitegrid")

        # Gráfico de dispersão com outliers destacados
        sns.scatterplot(
            data=df,
            x="Urbanization Rate (%)",
            y="Rent Index",
            hue="Outlier",
            palette={True: "blue", False: "red"},
            s=100,
            alpha=0.8,
            legend="auto"
        )

        # Linha de tendência (regressão linear)
        sns.regplot(
            data=df,
            x="Urbanization Rate (%)",
            y="Rent Index",
            scatter=False,
            color="black",
            line_kws={"linestyle": "--", "alpha": 0.5}
            
        )
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], color='black', linestyle='--', label='Linha de Tendência'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Outlier (False)'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Outlier (True)')
        ]

        # Posicionar a legenda
        plt.legend(handles=legend_elements, title="Legenda", bbox_to_anchor=(1.05, 1), loc='upper left')


        # Ajustes estéticos
        plt.title("Correlação entre Outliers de Aluguel e Taxa de Urbanização", fontsize=14)
        plt.xlabel("Taxa de Urbanização (%) K", fontsize=12)
        plt.ylabel("Índice de Aluguel (USD) K", fontsize=12)
        plt.show()

    def countries_growth(self, top_countries: pd.DataFrame, initial_year, final_year) -> None:
        plt.figure(figsize=(12, 6))
        plt.barh(top_countries['Country'], top_countries['Growth (%)'], color='skyblue')
        plt.xlabel('Crescimento Percentual (%)')
        plt.title(f'Países com Maior Aumento no Preço de Casas ({initial_year}–{final_year})')
        plt.gca().invert_yaxis()  # Países em ordem decrescente
        plt.show()

    def plot_index_house_price(self, df_sorted: pd.DataFrame) -> None:
        # Define o tamanho do gráfico
        plt.figure(figsize=(10, 6))

        # Cria o gráfico de barras horizontais
        plt.barh(df_sorted['Country_Year'], df_sorted['House Price Index'], color='skyblue')

        # Adiciona os rótulos e título
        plt.xlabel('House Price Index')
        plt.title('Índice de Preço das Casas por País e Ano')
        plt.tight_layout()

        # Exibe o gráfico
        plt.show()

    def plot_reason_price_income_house(self, reason_price_income: pd.DataFrame) -> None:
        plt.figure(figsize=(12, 8))
        bars = plt.barh(reason_price_income.index, reason_price_income['Value'],
                    color=plt.cm.Blues(np.linspace(0.3, 1, len(reason_price_income))))

        # Ajustes estéticos
        plt.title('Razão Preço-Acessibilidade por País', fontsize=14, pad=20, fontweight='semibold')
        plt.xlabel('Razão (Preço da Casa/Acessibilidade Anual)', fontsize=12)
        plt.ylabel('')
        plt.xlim(0, 18)

        # Remover bordas
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)

        # Adicionar valores
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 0.3, bar.get_y() + bar.get_height()/2,
                    f'{width:.1f}',
                    va='center', ha='left',
                    color='#2d3436', fontsize=10)

        # Linha de referência para limite de acessibilidade
        # plt.axvline(x=12, color='#e74c3c', linestyle='--', alpha=0.7, lw=1)
        # plt.text(12.2, 2, 'Limite de Acessibilidade', color='#e74c3c', va='center')

        plt.tight_layout()
        plt.show()        

    def plot_comparison_Affordability(self, df_combined: pd.DataFrame) -> None:

        plt.figure(figsize=(14, 8))
        countries = df_combined.index
        bar_width = 0.35
        positions = range(len(countries))

        # Plotar barras
        plt.bar(positions, df_combined['Value_compra'], width=bar_width, label='COMPRA (Price/Income)', color='#3498db')
        plt.bar([p + bar_width for p in positions], df_combined['Value_aluguel'], width=bar_width, label='ALUGUEL (Rent/Income)', color='#e74c3c')

        # Ajustar eixos e legendas
        plt.title('Comparação de Acessibilidade: Compra vs. Aluguel por País', fontsize=14)
        plt.xlabel('País', fontsize=12)
        plt.ylabel('Razão (Acessibilidade Normalizado)', fontsize=12)
        plt.xticks([p + bar_width/2 for p in positions], countries, rotation=45, ha='right')
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        for i, v in enumerate(df_combined['Value_compra']):
            plt.text(i - 0.1, v + 0.2, f'{v:.1f}', color='black')
        for i, v in enumerate(df_combined['Value_aluguel']):
            plt.text(i - 0, v + 0.2, f'{v:.1f}', color='black')
        # Ajustar layout
        plt.tight_layout()
        plt.show()