import pandas as pd
from prophet import Prophet
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go

# Load and preprocess data
df = pd.read_csv('train.csv')
df = df.rename(columns={'Date': 'ds', 'Weekly_Sales': 'y'})
df['ds'] = pd.to_datetime(df['ds'])
df = df.groupby('ds', as_index=False).sum()

# Load additional files
try:
    stores_df = pd.read_csv('stores.csv')
except FileNotFoundError:
    stores_df = pd.DataFrame()  # Handle missing stores.csv gracefully

# Check for the presence of the 'Store' column in stores.csv
if 'Store' not in stores_df.columns:
    stores_df['Store'] = 'Unknown'  # Fallback if 'Store' column is missing
    print("Warning: 'Store' column is missing, using default 'Unknown' value.")

# Fit Prophet model
model = Prophet(yearly_seasonality=True)
model.fit(df)

# App Initialization
app = Dash(__name__)
app.title = "Live Forecast Dashboard"

# Layout definition
app.layout = html.Div(style={'backgroundColor': '#121212', 'color': 'white', 'padding': '20px'}, children=[
    html.H1("📈 Weekly Sales Forecast Dashboard", style={'textAlign': 'center'}),

    # Date Picker for historical view
    html.Div([
        html.Label("Select Date Range:", style={'fontSize': '18px', 'textAlign': 'center'}),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=df['ds'].min().date(),
            end_date=df['ds'].max().date(),
            display_format='YYYY-MM-DD',
            style={
                'color': 'white',  # Text color for the picker
                'backgroundColor': 'orange',  # Full background color of the date picker
                'border': 'none',  # Remove the border of the component
                'padding': '10px',  # Optional: adds padding for better visual
                'borderRadius': '5px',  # Optional: adds rounded corners
                'fontSize': '16px'  # Optional: adjusts the font size for better readability
            }
        )
    ], style={'marginBottom': '30px', 'textAlign': 'center'}),  # Center the div and its content

    html.Div(id='forecast-summary'),

    # Tabs with corresponding graphs
    dcc.Tabs(id='tabs-content', children=[
        dcc.Tab(
            label='🟧 Main Forecast',
            children=[dcc.Graph(id='main-forecast')],
            style={'backgroundColor': 'orange', 'color': 'white', 'fontWeight': 'bold'},
            selected_style={'backgroundColor': 'orange', 'color': 'white', 'fontWeight': 'bold'}
        ),
        dcc.Tab(
            label='📉 Trend Component',
            children=[dcc.Graph(id='trend-component')],
            style={'backgroundColor': 'orange', 'color': 'white', 'fontWeight': 'bold'},
            selected_style={'backgroundColor': 'orange', 'color': 'white', 'fontWeight': 'bold'}
        ),
        dcc.Tab(
            label='🌦 Yearly Seasonality',
            children=[dcc.Graph(id='yearly-seasonality')],
            style={'backgroundColor': 'orange', 'color': 'white', 'fontWeight': 'bold'},
            selected_style={'backgroundColor': 'orange', 'color': 'white', 'fontWeight': 'bold'}
        ),
        dcc.Tab(
            label='📊 Forecast vs Actual',
            children=[dcc.Graph(id='forecast-vs-actual')],
            style={'backgroundColor': 'orange', 'color': 'white', 'fontWeight': 'bold'},
            selected_style={'backgroundColor': 'orange', 'color': 'white', 'fontWeight': 'bold'}
        )
    ])
])

# Callback to update forecasts based on user input
@app.callback(
    [Output('forecast-summary', 'children'),
     Output('main-forecast', 'figure'),
     Output('trend-component', 'figure'),
     Output('yearly-seasonality', 'figure'),
     Output('forecast-vs-actual', 'figure')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_forecast(start_date, end_date):
    # Filter data based on date range
    filtered_df = df[(df['ds'] >= start_date) & (df['ds'] <= end_date)]

    # Fit Prophet model on filtered data
    model = Prophet(yearly_seasonality=True)
    model.fit(filtered_df)

    # Create forecast for the selected date range
    future = model.make_future_dataframe(periods=52, freq='W')
    forecast = model.predict(future)
    last_date = filtered_df['ds'].max()
    future_forecast = forecast[forecast['ds'] > last_date]

    latest = future_forecast.tail(1).iloc[0]
    latest_date = latest['ds'].strftime('%Y-%m-%d')
    latest_sales = round(latest['yhat'], 2)

    # Summary Display
    summary = html.Div([
        html.Div([
            html.H3("🗓️ Forecast Date:"),
            html.P(f"{latest_date}", style={'fontSize': '22px'}),
        ], style={'width': '45%', 'display': 'inline-block'}),

        html.Div([
            html.H3("💵 Forecasted Sales:"),
            html.P(f"${latest_sales}", style={'fontSize': '22px'}),
        ], style={'width': '45%', 'display': 'inline-block'})
    ])

    # Main Forecast Graph
    main_forecast_fig = {
        'data': [
            go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='Overall Forecast', line=dict(color='#8ab4f8')),
            go.Scatter(x=future_forecast['ds'], y=future_forecast['yhat'], name='Forecast', line=dict(color='#ff6d00')),
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

    # Trend Component Graph
    trend_component_fig = {
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

    # Yearly Seasonality Graph
    monthly_effect = forecast.groupby(forecast['ds'].dt.month)['yearly'].mean().reindex(range(1, 13)).values
    month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    yearly_seasonality_fig = {
        'data': [
            go.Scatter(
                x=month_labels,
                y=monthly_effect,
                name='Yearly Seasonality',
                line=dict(color='#03dac6', width=3),
                mode='lines+markers',
                marker=dict(size=6),
                hovertemplate='Month: %{x}<br>Effect: %{y:.2f}<extra></extra>'
            )
        ],
        'layout': go.Layout(
            title='Yearly Seasonality Effect (Averaged by Month)',
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#121212',
            font=dict(color='white'),
            xaxis=dict(title='Month'),
            yaxis=dict(title='Effect', zeroline=True, showgrid=True, gridcolor='#333'),
            margin=dict(t=60, b=40, l=60, r=20)
        )
    }

    # Forecast vs Actual Graph (assuming actual sales data is available)
    actual_sales = df[df['ds'] <= last_date]
    forecast_vs_actual_fig = {
        'data': [
            go.Scatter(x=actual_sales['ds'], y=actual_sales['y'], name='Actual Sales', line=dict(color='#ff6347')),
            go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='Forecast', line=dict(color='#8ab4f8'))
        ],
        'layout': go.Layout(
            title='Forecast vs Actual Sales',
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#121212',
            font=dict(color='white'),
            xaxis=dict(title='Date'),
            yaxis=dict(title='Sales')
        )
    }

    return summary, main_forecast_fig, trend_component_fig, yearly_seasonality_fig, forecast_vs_actual_fig

# Run server
if __name__ == '__main__':
    app.run(debug=True)
