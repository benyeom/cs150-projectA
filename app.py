import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

path = "assets/ad_viz_plotval_data.csv"
df = pd.read_csv(path)

df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values(by="Date")

# Daily Data
fig_daily = px.line(df, x="Date", y="Daily Mean PM2.5 Concentration", title="<b>Daily PM2.5 Levels<b>")

# Weekly Data
df["Week"] = df["Date"].dt.to_period("W").apply(lambda r: r.start_time)
weekly_avg = df.groupby("Week")["Daily Mean PM2.5 Concentration"].mean().reset_index()
fig_weekly = px.line(weekly_avg, x="Week", y="Daily Mean PM2.5 Concentration", title="<b>Weekly PM2.5 Levels<b>", labels={"Daily Mean PM2.5 Concentration": "Weekly Mean PM2.5 Concentration"})

# Monthly Data
df["Month"] = df["Date"].dt.to_period("M").apply(lambda r: r.start_time)
monthly_avg = df.groupby("Month")["Daily Mean PM2.5 Concentration"].mean().reset_index()
fig_monthly = px.line(monthly_avg, x="Month", y="Daily Mean PM2.5 Concentration", title="<b>Monthly PM2.5 Levels<b>", labels={"Daily Mean PM2.5 Concentration": "Monthly Mean PM2.5 Concentration"})

# Set y-axis title font size inline
fig_daily["layout"]["yaxis"]["title"]["font"] = {"size": 18}
fig_weekly["layout"]["yaxis"]["title"]["font"] = {"size": 18}
fig_monthly["layout"]["yaxis"]["title"]["font"] = {"size": 18}

# App Layout ***************************************************************************
stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(__name__, external_stylesheets=stylesheets)

app.layout = html.Div([
    html.H1("AIR QUALITY IN SANTA BARBARA",
            style={
                "text-align": "center",
                "padding": "50px 0",
                "margin": "50px 0",
                "font-size": "48px",
                "font-weight": "bold",
                "font-family": "Arial, sans-serif",
                "text-transform": "uppercase",}),
    dcc.Dropdown(
        id="my-dropdown",
        options=[
            {"label": "Daily", "value": "daily"},
            {"label": "Weekly", "value": "weekly"},
            {"label": "Monthly", "value": "monthly"}
        ],
        value="daily",
        clearable=False,
        style={"font-weight": "bold", "font-size": "20px", "width": "50%", "margin": "0 auto"}
    ),
    dcc.Graph(id="output-graph"),
    html.P(
        "Note: PM2.5 levels are measured in micrograms per cubic meter (µg/m³). Lower values indicate better air quality.",
        style={"text-align": "center", "font-size": "16px", "margin-top": "10px", "color": "gray"})
])

# Callbacks ****************************************************************************
@app.callback(
    Output("output-graph", "figure"),
    Input("my-dropdown", "value")
)
def update_graph(selected_value):
    if selected_value == "daily":
        return fig_daily
    elif selected_value == "weekly":
        return fig_weekly
    elif selected_value == "monthly":
        return fig_monthly
    return fig_daily

if __name__ == "__main__":
    app.run_server(debug=True)



