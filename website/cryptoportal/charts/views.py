from django.shortcuts import render
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import yfinance as yf

# Create your views here.


def intro(req):
    _stock_info = yf.Ticker("^NSEI")
    df = _stock_info.history(period="max")
    df = df.drop(["Dividends", "Stock Splits"], axis=1)
    df = df[df.index > "1990-01-01"][df.index < "2020-03-01"]
    df = df[df["Volume"] > 0]

    fig = go.Figure(data=go.Scatter(x=df.index, y=df["Close"]))

    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(
        go.Scatter(x=df.index, y=df["Close"], name="Price"), secondary_y=False
    )
    fig2.add_trace(go.Bar(x=df.index, y=df["Volume"], name="Volume"), secondary_y=True)
    fig2.update_yaxes(range=[0, 700000000], secondary_y=True)
    fig2.update_yaxes(visible=False, secondary_y=True)

    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    fig3.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            close=df["Close"],
            high=df["High"],
            low=df["Low"],
        ),
        secondary_y=False,
    )
    fig3.add_trace(
        go.Scatter(x=df.index, y=df["Close"].rolling(20).mean(), name="20D-MA"),
        secondary_y=False,
    )
    fig3.add_trace(
        go.Scatter(x=df.index, y=df["Close"].rolling(100).mean(), name="100D-MA"),
        secondary_y=False,
    )
    fig3.add_trace(go.Bar(x=df.index, y=df["Volume"], name="Volume"), secondary_y=True)
    fig3.update_yaxes(range=[0, 700000000], secondary_y=True)
    fig3.update_yaxes(visible=False, secondary_y=True)

    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    fig4.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            close=df["Close"],
            high=df["High"],
            low=df["Low"],
        ),
        secondary_y=False,
    )
    fig4.add_trace(
        go.Scatter(x=df.index, y=df["Close"].rolling(20).mean(), name="20D-MA"),
        secondary_y=False,
    )
    fig4.add_trace(
        go.Scatter(x=df.index, y=df["Close"].rolling(100).mean(), name="100D-MA"),
        secondary_y=False,
    )
    fig4.add_trace(go.Bar(x=df.index, y=df["Volume"], name="Volume"), secondary_y=True)
    fig4.update_yaxes(range=[0, 700000000], secondary_y=True)
    fig4.update_yaxes(visible=False, secondary_y=True)
    fig4.update_layout(xaxis_rangeslider_visible=False)

    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    fig2.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    fig3.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    fig4.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    context = {
        "basic": fig.to_html(full_html=False),
        "scatter": fig2.to_html(full_html=False),
        "candle_range": fig3.to_html(full_html=False),
        "candle": fig4.to_html(full_html=False),
    }
    return render(req, "intro.html", context=context)
