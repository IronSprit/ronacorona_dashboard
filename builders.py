from dash import Dash, html, dcc

def make_table(data_frame):
    return html.Table(
        children=[
            html.Thead(
                # style={"paddingBottom":"5px"},
                children=[
                    html.Tr(
                        className="data-header",
                        style={"textAlign":"left"},
                        children=[
                        html.Th(column_name.replace("_", " ")) for column_name in data_frame.columns
                        ]

                        )
                ]
            ),

            html.Tbody(
                style={"textAlign":"left"},
                children=[
                    html.Tr(
                        className="data-body",
                        children=[
                            html.Td(cell) for cell in row 
                            ]
                    ) for row in data_frame.values
                ]
            )
            ])
                            