# AED-Mercado-Imobiliario

# 🌍 Global Housing Market Analysis (2015-2024)

Análise do mercado imobiliário global com foco em tendências de preços, acessibilidade e identificação de padrões sazonais.

## 📦 Módulos Principais

### `preprocessing.py` (Pré-processamento de Dados)
| Método                      | Descrição                                          |
|-----------------------------|---------------------------------------------------|
| `__init__`                  | Carrega o dataset do caminho especificado         |
| `verify_nullable`           | Retorna contagem de valores nulos por coluna      |
| `get_unique_column`         | Acessa colunas específicas com métodos opcionais (`mean`, `median`, etc) |
| `select_country`            | Filtra países específicos (padrão: economias principais) |
| `get_correlation_dataset`   | Retorna matriz de correlação entre variáveis-chave|
| `get_values_outliers`       | Identifica outliers no Rent Index usando Z-Score  |
| `get_best_countries_with_growth` | Ranking de países por crescimento imobiliário    |
| `years_fall_prices`         | Identifica anos com quedas de preços por país     |
| `get_df_reason_price_income`| Calcula razão preço/renda para compra de imóveis  |
| `get_df_buy_vs_rent`        | Compara métricas de compra vs aluguel             |

### `plotting.py` (Visualizações)
| Método                      | Descrição                                          |
|-----------------------------|---------------------------------------------------|
| `plot_Outliers`             | Gráfico de dispersão com outliers e mediana       |
| `plot_graphic_dispersion`   | Correlação entre urbanização e preços de aluguel  |
| `countries_growth`          | Ranking de crescimento imobiliário em barras      |
| `plot_index_house_price`    | Índice de preços de casas por país/ano            |
| `plot_reason_price_income_house` | Razão preço/renda horizontal com limite de acessibilidade |
| `plot_comparison_Affordability` | Comparação compra vs aluguel em barras agrupadas |

## 🚀 Como Executar

1. **Instalação**:
```bash
git clone [seu-repositorio]
pip install pandas matplotlib numpy scipy seaborn
 -- run AED - Mercado Imobiliario.ipynb
