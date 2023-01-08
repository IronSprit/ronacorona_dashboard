# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

from dash.dependencies import Input, Output

from data import countries_dataframe, total_dataframe, get_countries_name, make_global_df, make_country_df
from builders import make_table

stylesheets = ["https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css", "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap"]

app = Dash(__name__, external_stylesheets=stylesheets)


data_view = {"Confirmed": ":, 2f",
              "Deaths": ":, 2f",
              "Recovered": True,
             "Country_Region": False}

bubble_map = px.scatter_geo(countries_dataframe, color="Confirmed", 
                            locations="Country_Region", locationmode="country names", 
                            size= "Confirmed", size_max=40,
                            template="plotly_dark", 
                            # projection="orthographic",
                            color_continuous_scale=px.colors.sequential.Oryel,
                            title="Confirmed By Country",
                            hover_data = data_view
                            )

bar_graph = px.bar(total_dataframe, x='condition', y='count', title="Total Global Cases", hover_data={'count':':,'},
                            labels={
                                "condition" : "Condition",
                                "count":"Count",
                                "color":"Condition"
                            },
                            # color=["Confirmed", "Deaths", "Recovered"],
                            template="plotly_dark"
                )

bar_graph.update_traces(marker_color=["#e74c3c", "#2980b9", "#f1c40f"])

# bar_graph.update_layout(xaxis=dict(title="Condition"), yaxis=dict(title="Count")) ->위에서 labels로도 쓸 수 있음.

app.layout = html.Div(
className="grid-body",
style={"textAlign":"center", "minHeight":"100vh", "backgroundColor":"black", "color":"white", "fontFamily":"Open Sans, sans-serif"}, 
children=[
    html.Header(
        style={"textAlign":"center"}, 
        children=[html.H1("Corona Dashboard", style={"fontSize": "30px"})]
        ), 
    html.Div(
            className="grid-top",
            children=[
                html.Div(className="data-bubble", children=[dcc.Graph(figure=bubble_map)]),
                html.Div(className="data-table", children=[make_table(countries_dataframe)]),                
            ]
        ),
    html.Div(       
                className="grid-bottom",
                children=[
                html.Div(className="data-bar", children=[dcc.Graph(figure=bar_graph)]),
                html.Div(className="data-line", children=[
                    # dcc.Input(placeholder="What are you doing?", id="hello-input"),
                    html.Div(className="data-line__top", children=[#html.H1(children=["Test"], id="hello-output"), 
                    dcc.Dropdown(id="country", options=get_countries_name()),]),
                    html.Div(className="data-line__bottom", children=[dcc.Graph(id="contry_output")]),
                    ]),
            ]
        ),
],
)

@app.callback(
    Output("contry_output", "figure"), #id: contry_output 에  property : figure 를 적용한다.
    [
        Input("country", "value") #id: country의  property : value 가 들어올거다.
    ]
)

# @app.callback(
#     Output("hello-output", "children"),
#     [
#         Input("hello-input", "value")
#     ]
# )

def update_hello(value):
    if value: #값이 있으면.
        df = make_country_df(value)
    else:
        df = make_global_df()

    line_fg = px.line(df, x='date', y=['confirmed', 'deaths', 'recovered'], labels={
    'value':'Cases', 'variable':'Condition','date':'Date'}, hover_data={'value':":,", "variable":False, "date":False
                                                                       }, template="plotly_dark")
    line_fg.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    line_fg.update_layout(
                  xaxis_rangeselector_font_color='white',
                  xaxis_rangeselector_activecolor='red',
                  xaxis_rangeselector_bgcolor='green',
                 )
    # 이렇게 하는 방법도 있고  go.Scatter 를 쓰는 방법도 있음. plotly.express 만으로는 힘듦.
    line_fg["data"][0]["line"]["color"] = "#e74c3c"
    line_fg["data"][1]["line"]["color"] = "#2980b9"
    line_fg["data"][2]["line"]["color"] = "#f1c40f"

    return line_fg
        

if __name__ == '__main__':
    app.run_server(host="192.168.83.147", debug=True)