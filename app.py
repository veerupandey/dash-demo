from click import style
import plotly_express as px
from dash import Dash, html, dcc, Input, Output
import altair as alt

# gapminder datset
gapminder = px.data.gapminder()

# Define app
app = Dash(
    __name__,
    external_stylesheets=["https://www.google.com/css/maia.css"],
)
server = app.server
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

# Set app
app.layout = html.Div(
    [
        html.Iframe(
            id="scatter",
            style={
                "border-width": "0",
                "width": "200%",
                "height": "400px",
                "display": "block",
            },
        ),
        html.Div(
            [
                dcc.Slider(
                    id="year",
                    min=1952,
                    max=2007,
                    step=5,
                    marks={x: str(x) for x in range(1952, 2008, 5)},
                )
            ],
            style={
                "width": "600px",
                "display": "block",
                "background-color": "azure",
                "opacity": "0.8",
                "transition": "opacity .2s",
                "font-weight": "bold",
                "font-size": "20px",
            },
        ),
    ]
)


@app.callback(Output("scatter", "srcDoc"), [Input("year", "value")])
def altair_fig(year):
    df = gapminder.query("year == %d" % (year or 1952))
    return (
        alt.Chart(df, height=250, width=400)
        .mark_circle()
        .encode(
            alt.X("gdpPercap:Q", scale=alt.Scale(type="log")),
            alt.Y("lifeExp:Q", scale=alt.Scale(zero=False)),
            size="pop:Q",
            color="continent:N",
            tooltip=list(df.columns),
        )
        .interactive()
        .properties(title="GDP vs Lifeexpectancy")
        .to_html()
    )


if __name__ == "__main__":
    app.run_server(debug=True)
