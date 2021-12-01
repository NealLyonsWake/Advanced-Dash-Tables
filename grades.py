# import
import dash
from dash import dash_table as dt
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd

# import dataframe
grades_df = pd.read_csv("data/grades.csv")
# create name selection variable
names_for_options = grades_df["Name"]
filter_by_name = grades_df[grades_df["Name"] == ""]

# dash initialisation
app = dash.Dash("", external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    html.Div(
        [
            html.H1("Grade Checker"),
            html.Br(),
            html.Br(),
            dcc.Dropdown(
                options=[{"label": i, "value": i} for i in names_for_options],
                id="name-menu",
            ),
            html.Br(),
            html.Br(),
            html.Button("Find my grade", id="find-button", n_clicks=0),
            html.Br(),
            html.Br(),
            dt.DataTable(
                id="grades-output",
                columns=[{"name": i, "id": i} for i in filter_by_name.columns],
                data=filter_by_name.to_dict(orient="records"),
                style_cell={'textAlign': 'center'},
            ),
        ],
        className="container",
    ),
    className="main-container",
)


#  callback
@app.callback(
    Output(component_id="grades-output", component_property="data"),
    Input(component_id="find-button", component_property="n_clicks"),
    State(component_id="name-menu", component_property="value"),
)
def request_grades(on_click, name_selected):
    if name_selected is not None:
        filter_by_name = pd.DataFrame(grades_df[grades_df["Name"] == name_selected])
        return filter_by_name.to_dict(orient="records")
    else:
        filter_by_name = grades_df[grades_df["Name"] == ""]
        return filter_by_name.to_dict(orient="records")


# run
app.run_server(debug=True)
