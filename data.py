import pandas as pd

daily_dataframe = pd.read_csv("data/daily_report.csv")

total_dataframe = daily_dataframe[["Confirmed", "Deaths", "Recovered"]].sum().reset_index(name="count")

total_dataframe = total_dataframe.rename(columns={'index':"condition"})


# countries_dataframe = daily_dataframe[["Confirmed", "Deaths", "Recovered"]].sum().reset_index(name="count")
countries_dataframe = daily_dataframe[["Country_Region", "Confirmed", "Deaths", "Recovered"]]

# countries_dataframe = countries_dataframe.rename(columns={'index':"condition"})
#countries_dataframe = countries_dataframe.groupby("Country_Region").sum()
countries_dataframe = countries_dataframe.groupby("Country_Region").sum().sort_values(by="Confirmed", ascending=False).reset_index()


# print(type(countries_dataframe))

# print(countries_dataframe)

conditions = ["confirmed", "deaths", "recovered"]

def make_global_df():
    def make_df(condition):
        daily_dataframe = pd.read_csv(f"data/time_{condition}.csv")
        
        confirmed_dataframe = daily_dataframe.drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1).sum().reset_index(name=condition)
        confirmed_dataframe = confirmed_dataframe.rename(columns={'index':'date'})
        
        confirmed_dataframe['date'] = pd.to_datetime(confirmed_dataframe['date'])
        return confirmed_dataframe

    fianl_df = None
    for condition in conditions:
        condition_df = make_df(condition)
        
        if fianl_df is None:
            fianl_df = condition_df
        else:
            fianl_df = fianl_df.merge(condition_df) 
    return fianl_df

def make_country_df(country):
    def make_df(condition, country):
        daily_dataframe = pd.read_csv(f"data/time_{condition}.csv")
        view = daily_dataframe.loc[daily_dataframe["Country/Region"] == country]
        view = view.drop(columns={'Province/State', 'Country/Region', 'Lat', 'Long'}).sum().reset_index(name=condition).rename(columns={'index':'date'})
        
        view['date'] = pd.to_datetime(view['date'])
        return view

    fianl_df = None
    for condition in conditions:
        condition_df = make_df(condition, country)

        if fianl_df is None:
            fianl_df = condition_df
        else:
            fianl_df = fianl_df.merge(condition_df)

    return fianl_df

# print(make_country_df("Albania"))

def get_countries_name():
    data = countries_dataframe.sort_values("Country_Region").reset_index()
    data = data["Country_Region"]

    dropdown_option = {country:country for country in data}

    return dropdown_option

