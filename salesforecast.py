import pandas as pd
from prophet import Prophet
from dash import Dash, dcc, html
import plotly.graph_objs as go

# Load and preprocess data
df = pd.read_csv('train.csv')
df = df.rename(columns={'Date': 'ds', 'Weekly_Sales': 'y'})
df['ds'] = pd.to_datetime(df['ds'])
df = df.groupby('ds', as_index=False).sum()

# Fit Prophet model
model = Prophet(yearly_seasonality=True)
model.fit(df)

# Forecasting
future = model.make_future_dataframe(periods=10, freq='W')
forecast = model.predict(future)
last_date = df['ds'].max()
future_forecast = forecast[forecast['ds'] > last_date]

# Summary values
latest = future_forecast.tail(1).iloc[0]
latest_date = latest['ds'].strftime('%Y-%m-%d')
latest_sales = round(latest['yhat'], 2)

# App Initialization
app = Dash(__name__)
app.title = "Live Forecast Dashboard"

# Layout
app.layout = html.Div(style={'backgroundColor': '#121212', 'color': 'white', 'padding': '20px'}, children=[
    html.H1("📈 Weekly Sales Forecast Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Div([
            html.H3("📅 Forecast Date:"),
            html.P(f"{latest_date}", style={'fontSize': '22px'}),
        ], style={'width': '45%', 'display': 'inline-block'}),

        html.Div([
            html.H3("💵 Forecasted Sales:"),
            html.P(f"${latest_sales}", style={'fontSize': '22px'}),
        ], style={'width': '45%', 'display': 'inline-block'})
    ]),

    html.Br(), html.Hr(),

    dcc.Tabs([
        dcc.Tab(label='🟦 Main Forecast',
                children=[
                    dcc.Graph(
                        figure={
                            'data': [
                                go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='Overall Forecast', line=dict(color='#8ab4f8')),
                                go.Scatter(x=future_forecast['ds'], y=future_forecast['yhat'], name='10-week Forecast', line=dict(color='#ff6d00')),
                                go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], name='Upper Bound', line=dict(color='#4a4a4a', dash='dot'), showlegend=False),
                                go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], name='Lower Bound', fill='tonexty', fillcolor='rgba(74,74,74,0.3)', line=dict(color='#4a4a4a'), showlegend=False)
                            ],
                            'layout': go.Layout(
                                title='Weekly Sales Forecast',
                                plot_bgcolor='#1e1e1e',
                                paper_bgcolor='#121212',
                                font=dict(color='white'),
                                xaxis=dict(title='Date'),
                                yaxis=dict(title='Sales')
                            )
                        }
                    )
                ],
                style={'backgroundColor': 'orange', 'color': 'white', 'fontWeight': 'bold'},
                selected_style={'backgroundColor': '#ff9800', 'color': 'white', 'fontWeight': 'bold'}
        ),

        dcc.Tab(label='📉 Trend Component',
                children=[
                    dcc.Graph(
                        figure={
                            'data': [
                                go.Scatter(x=forecast['ds'], y=forecast['trend'], name='Trend', line=dict(color='#03dac6')),
                                go.Scatter(x=future_forecast['ds'], y=future_forecast['trend'], name='Future Trend', line=dict(color='#bb86fc'))
                            ],
                            'layout': go.Layout(
                                title='Trend Component',
                                plot_bgcolor='#1e1e1e',
                                paper_bgcolor='#121212',
                                font=dict(color='white'),
                                xaxis=dict(title='Date'),
                                yaxis=dict(title='Trend')
                            )
                        }
                    )
                ],
                style={'backgroundColor': 'orange', 'color': 'white', 'fontWeight': 'bold'},
                selected_style={'backgroundColor': '#ff9800', 'color': 'white', 'fontWeight': 'bold'}
        ),

        dcc.Tab(label='🌦 Yearly Seasonality',
                children=[
                    dcc.Graph(
                        figure={
                            'data': [
                                go.Scatter(
                                    x=forecast['ds'].dt.dayofyear,
                                    y=forecast['yearly'],
                                    name='Yearly Seasonality',
                                    line=dict(color='#03dac6')
                                )
                            ],
                            'layout': go.Layout(
                                title='Yearly Seasonality Effect',
                                plot_bgcolor='#1e1e1e',
                                paper_bgcolor='#121212',
                                font=dict(color='white'),
                                xaxis=dict(title='Day of Year'),
                                yaxis=dict(title='Effect')
                            )
                        }
                    )
                ],
                style={'backgroundColor': 'orange', 'color': 'white', 'fontWeight': 'bold'},
                selected_style={'backgroundColor': '#ff9800', 'color': 'white', 'fontWeight': 'bold'}
        )
    ])
])

# Run server
if __name__ == '__main__':
    app.run(debug=True)