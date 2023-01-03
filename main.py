import pandas as pd

daily_dataframe = pd.read_csv("data/daily_report.csv")

# countries_dataframe = daily_dataframe[["Confirmed", "Deaths", "Recovered"]].sum().reset_index(name="count")
countries_dataframe = daily_dataframe[["Country_Region", "Confirmed", "Deaths", "Recovered"]]

# countries_dataframe = countries_dataframe.rename(columns={'index':"condition"})
#countries_dataframe = countries_dataframe.groupby("Country_Region").sum()
countries_dataframe = countries_dataframe.groupby("Country_Region").sum().reset_index()


print(type(countries_dataframe))

print(countries_dataframe)