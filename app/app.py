# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px

# app = Dash(__name__)

# # assume you have a "long-form" data frame
# # see https://plotly.com/python/px-arguments/ for more options
# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

# app.layout = html.Div(children=[
#     html.H1(children='Hello Dash!!', style={'textAlign': 'center', 'color': '#7FDBFF'}),

#     html.Div(children='''
#         Dash: A web application framework for your data.
#     '''),

#     dcc.Graph(
#         id='example-graph',
#         figure=fig
#     )
# ])

# df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')


# def generate_table(dataframe, max_rows=10):
#     return html.Table([
#         html.Thead(
#             html.Tr([html.Th(col) for col in dataframe.columns])
#         ),
#         html.Tbody([
#             html.Tr([
#                 html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#             ]) for i in range(min(len(dataframe), max_rows))
#         ])
#     ])


# app = Dash(__name__)

# app.layout = html.Div([
#     html.H4(children='US Agriculture Exports (2011)'),
#     generate_table(df)
# ])

# instantiate a Dash instance
app = Dash(__name__, suppress_callback_exceptions=True)

# make up some data
df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
    }
)

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

# Define a plotly bar chart.
fig = px.bar(df, x="Fruit", y="Amount", color="City")
graph_layout = html.Div(
    children=[
        html.H1(
            children="Hello Dash!",
            style={"textAlign": "center"},
        ),
        dcc.Dropdown(
            options=df["City"].unique(),
            id="dropdown-filter",
            style={"padding-left": 10, "padding-right": 10},
        ),
        html.Div(
            children="""
                Dash: A web application framework for your data.
        """,
            style={"text-align": "center"},
        ),
        dcc.Graph(id="example-graph", figure=fig),
        dcc.Link(
            children=html.Button("Go To Another Page"),
            href="/another_page",
            id="go-to-another-page",
            title="Go to Another Page!",
        ),
    ]
)

other_page_layout = html.Div(
    [
        html.H1("You are on another page"),
        dcc.Link(
            children=html.Button("Go Back to Graph!"),
            href="/graph",
            id="back-to-graph",
            title="Return to Graph",
        ),
    ]
)


@app.callback(
    Output(component_id="example-graph", component_property="figure"),
    Input(component_id="dropdown-filter", component_property="value"),
)
def update_graph(value):
    if value is not None:
        filtered_df = df[df["City"] == value]
        filtered_fig = px.bar(filtered_df, x="Fruit", y="Amount", color="City")
        return filtered_fig
    return px.bar(df, x="Fruit", y="Amount", color="City")


@callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/graph":
        return graph_layout
    else:
        return other_page_layout

server = app.server
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
