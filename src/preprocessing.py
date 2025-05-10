import pandas as pd
import numpy as np
import os

# Carregando base de dados
class Preprocess():
    def __init__(self, DIRECTORY: os.PathLike):
        #self.directory = DIRECTORY
        self.df = pd.read_csv(DIRECTORY, index_col=1)

    def verify_nullable(self) -> pd.Series:
       return self.df.isnull().sum()
    
    def get_df(self) -> pd.DataFrame:
        return self.df
    
    def get_unique_column(self, column: str, method:str = None) -> pd.Series:
        try:
            column = self.df[f"{column}"]
        except: return f"Column: {column} não encontrada"
        match method:
            case None: return column
            case _:
                try: run_method = getattr(column, method)
                except Exception as e: return f"Column: {column} não encontrada ou Method:{method} nao encontrado\nErro:{e}"
                return run_method()

    def select_country(self, country:list = "standart") -> pd.DataFrame:
        match country:
            case "standart":
                df_country = self.df[self.df["Country"].isin(["Brazil", "USA", "Canada", "France", "Spain"])]
            case _:
                df_country = self.df[self.df["Country"].isin(country)]
        return df_country
    
    def get_correlation_dataset(self):
        return self.df[['Affordability Ratio', 'Mortgage Rate (%)', 'Construction Index', 'Urbanization Rate (%)', "House Price Index"
                 ,"Rent Index"]].corr()
    
    def get_values_outliers(self) -> dict:
        from scipy.stats import zscore
        self.df["Z-Score"] = zscore(self.df["Rent Index"])
        self.df["Outlier"] = (self.df["Z-Score"].abs() > 3)  # Outliers além de 3
        import seaborn as sns
        import matplotlib.pyplot as plt
        #region Graphic distribuicao z-scxore
        sns.histplot(self.df["Z-Score"], kde=True)
        plt.axvline(x=3, color='red', linestyle='--', label='Limite Outlier (Z=3)')
        plt.axvline(x=-3, color='red', linestyle='--')
        plt.legend()
        plt.title("Distribuição do Z-Score do Rent Index")
        plt.show()
        #endregion
        # Configurar subplots lado a lado
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        # Histograma com KDE
        sns.histplot(self.df["Rent Index"], kde=True, color="blue", ax=axes[0])
        axes[0].set_title("Distribuição do Rent Index (Histograma)")
        axes[0].set_xlabel("Rent Index")
        axes[0].set_ylabel("Frequência")
        axes[0].grid(True, linestyle='--', alpha=0.6)

        # Boxplot
        sns.boxplot(data=self.df, x="Rent Index", color="orange", ax=axes[1])
        axes[1].set_title("Distribuição do Rent Index (Boxplot)")
        axes[1].set_xlabel("Rent Index")
        axes[1].grid(True, linestyle='--', alpha=0.6)

        plt.tight_layout()
        plt.show()

        q1 = self.df["Rent Index"].quantile(0.25)
        q3 = self.df["Rent Index"].quantile(0.75)
        IQR = q3 - q1 #range interquatil, to verify outliers
        limit_inferior = q1 - (1.5 * IQR)
        limit_superior = q3 - (1.5 * IQR)
        return {"limit_inferior":limit_inferior, "limit_superior":limit_superior}
    
    def get_best_countries_with_growth(self, inital_year:int, final_year:int, quantity:int) -> pd.Series:
        year_inial = self.df[self.df.index == int(inital_year)][["Country","House Price Index"]]
        year_final =  self.df[self.df.index == int(final_year)][["Country","House Price Index"]]

        merged = pd.merge(year_inial, year_final, on="Country", suffixes=(f"_{inital_year}", f"_{final_year}")).dropna()
        merged["Growth (%)"] = ((merged[f"House Price Index_{final_year}"]/merged[f"House Price Index_{inital_year}"]) -1) * 100
        # best = merged.sort_values('Growth (%)', ascending=False).iloc[0]
        return merged.sort_values('Growth (%)', ascending=False).head(quantity)

    def years_fall_prices(self, country: list | str = "standart") -> pd.Series:
        match country:
            case "standart":
                developed_economies = [
                            "Canada",
                            "USA",
                            "UK",
                            "France",
                            "Germany",
                            "Australia",
                            "Japan",
                            "Switzerland",
                            "Sweden",
                            "Netherlands",
                            "Italy",
                            "Spain",
                            "South Korea"
                        ]
            case _:
                developed_economies = country

        countries_fall = self.df[self.df["Country"].isin(developed_economies)]
        country_fall = countries_fall.groupby(["Country", "Year"])["House Price Index"].min()
        # Encontrar ano e valor mínimo
        min_indices = country_fall.groupby("Country").idxmin()
        # print(min_indices)
        fall_prices = country_fall.loc[min_indices.values]
        df_reset = pd.DataFrame(fall_prices.reset_index())
        # Criar labels personalizados (País + Ano)
        df_reset['Country_Year'] = df_reset['Country'] + ' (' + df_reset['Year'].astype(str) + ')'
        # Ordenar os dados pelo índice
        return  df_reset.sort_values('House Price Index', ascending=False)
    
    def __get_df_buy(self) -> pd.DataFrame:#reason_price_income
        affordability_ratio = self.df.groupby("Country")["Affordability Ratio"].max()
        reason_price_income = self.df.groupby("Country")["House Price Index"].mean() / affordability_ratio
        reason_price_income = pd.DataFrame(reason_price_income).reset_index().set_index("Country")
        reason_price_income.columns = ['Value']  # Renomear colunas
        return reason_price_income
    
    def __get_df_rent(self) -> pd.DataFrame:
        rent_median_country = self.df.groupby("Country")["Rent Index"].median()
        affordability_ratio = self.df.groupby("Country")["Affordability Ratio"].max()
        reason_rent_income =  pd.DataFrame(rent_median_country / affordability_ratio).reset_index().set_index("Country")
        reason_rent_income.columns = ["Value"]
        return reason_rent_income
     
    def get_df_reason_price_income(self) -> pd.DataFrame:
        affordability_ratio = self.df.groupby("Country")["Affordability Ratio"].max()
        reason_price_income = self.df.groupby("Country")["House Price Index"].mean() / affordability_ratio
        reason_price_income = pd.DataFrame(reason_price_income).reset_index().set_index("Country")
        reason_price_income.columns = ['Value']  # Renomear colunas
        # Ordenar os dados
        return reason_price_income.sort_values('Value', ascending=True)
    
    def get_df_buy_vs_rent(self) -> pd.DataFrame:
        return pd.merge(self.__get_df_buy(), self.__get_df_rent(), left_index=True, right_index=True, suffixes=('_buy', '_rent'))
