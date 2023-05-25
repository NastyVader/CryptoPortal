import datetime as dt
import os
from datetime import datetime

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import yfinance as yf
from django.shortcuts import render
from plotly.subplots import make_subplots
from statsmodels.tsa.arima.model import ARIMA

# Create your views here.


def intro(req):
    if req.POST:
        if req.POST.get("coin"):
            chart = req.POST.get("coin")
            _stock_info = yf.Ticker(chart + "-USD")
        else:
            chart = "BTC"
            _stock_info = yf.Ticker("BTC-USD")
        pass
    else:
        chart = "BTC"
        _stock_info = yf.Ticker("BTC-USD")
    df = _stock_info.history(period="max")
    df["Close"] *= 82.54
    df["Open"] *= 82.54
    df["High"] *= 82.54
    df["Low"] *= 82.54
    df["day_return"] = df["Close"].pct_change()
    df = df.iloc[1:]
    # df = df.drop(["Dividends", "Stock Splits"], axis=1)
    df = df[df["Volume"] > 0]
    print(chart)
    print(df.head())
    pred_list = []
    with open(
        f"C:\\Users\\ronad\\Downloads\\CryptoPortal\\website\\cryptoportal\\charts\\static\\Models\\{chart}.txt",
        "a",
    ):
        pass
    with open(
        f"C:\\Users\\ronad\\Downloads\\CryptoPortal\\website\\cryptoportal\\charts\\static\\Models\\date.txt",
        "r+",
    ) as f, open(
        f"C:\\Users\\ronad\\Downloads\\CryptoPortal\\website\\cryptoportal\\charts\\static\\Models\\{chart}.txt",
        "r+",
    ) as c:
        date = f.readlines()
        today = str(datetime.now().date())
        if len(date) == 0:
            f.seek(0)
            f.truncate()
            f.write(today)
            pred_list = get_preds_list(df, chart)
            c.seek(0)
            c.truncate()
            c.writelines(pred_list)
        else:
            pred_list = c.readlines()
            if len(pred_list) == 0:
                pred_list = get_preds_list(df, chart)
                c.seek(0)
                c.truncate()
                c.writelines(pred_list)
            if date[0] != today:
                f.seek(0)
                f.truncate()
                f.write(today)
                pred_list = get_preds_list(df, chart)
                c.seek(0)
                c.truncate()
                c.writelines(pred_list)
    # date_list = [dt.timedelta(days=x) - base for x in range(20)]
    date_list = [dt.date.today() + dt.timedelta(days=i) for i in range(1, 21)]
    pred_df = pd.DataFrame(
        {
            "price_return": [float(i) for i in pred_list],
        },
        index=date_list,
    )

    fig = go.Figure(data=go.Scatter(x=df.index, y=df["day_return"]))

    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(
        go.Scatter(x=df.index, y=df["Close"], name="Price"), secondary_y=False
    )
    fig2.add_trace(go.Bar(x=df.index, y=df["Volume"], name="Volume"), secondary_y=True)
    fig2.update_yaxes(range=[0, df["Volume"].max() * 10], secondary_y=True)
    fig2.update_yaxes(visible=False, secondary_y=True)
    fig2.update_layout(
        title=chart,
        xaxis_title="Time",
        yaxis_title="INR",
    )

    pred = make_subplots(specs=[[{"secondary_y": True}]])
    # pred.add_trace(
    #     go.Scatter(x=list(range(len(pred_list))), y=pred_list, name="Predicted"),
    #     secondary_y=False,
    # )
    pred.add_trace(
        go.Scatter(x=pred_df.index, y=pred_df["price_return"], name="Predicted"),
        secondary_y=False,
    )
    # pred.add_trace(
    #     go.Scatter(
    #         x=list(range(len(pred_list) - 20)), y=pred_list[:20], name="Previous"
    #     ),
    #     secondary_y=True,
    # )
    pred.update_yaxes(range=[-0.15, 0.15], secondary_y=True)
    pred.update_yaxes(visible=False, secondary_y=True)
    pred.update_layout(
        title=chart,
        xaxis_title="Time",
        yaxis_title="Price Return",
    )

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
    fig4.update_yaxes(range=[0, df["Volume"].max() * 10], secondary_y=True)
    fig4.update_layout(
        title=chart,
        xaxis_title="Time",
        yaxis_title="INR",
    )
    fig4.update_yaxes(visible=False, secondary_y=True)
    fig4.update_layout(xaxis_rangeslider_visible=False)

    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    fig2.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    pred.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    fig4.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

    context = {
        "basic": fig.to_html(full_html=False, default_width="100%", default_height=700),
        "scatter": fig2.to_html(
            full_html=False, default_width="100%", default_height=700
        ),
        "scatter_pred": pred.to_html(
            full_html=False, default_width="100%", default_height=700
        ),
        "candle": fig4.to_html(
            full_html=False, default_width="100%", default_height=700
        ),
        "coins": ["BTC", "ETH", "USDT", "BNB"],
        "coins2": ["USDC", "XRP", "ADA", "MATIC"],
        "chart": chart,
    }
    return render(req, "intro.html", context=context)


def login(req):
    return render(
        req,
        "login.html",
    )


def get_preds_list(df, chart):
    steps = 20
    df = pd.DataFrame(df.loc[:, "day_return"])
    dr = list(df["day_return"])[-200:]
    if os.path.exists(
        f"C:\\Users\\ronad\\Downloads\\CryptoPortal\\website\\cryptoportal\\charts\\static\\Models\\{chart}.sav"
    ):
        loaded_model = joblib.load(
            f"C:\\Users\\ronad\\Downloads\\CryptoPortal\\website\\cryptoportal\\charts\\static\\Models\\{chart}.sav"
        )
    else:
        loaded_model = ARIMA(
            dr,
            order=(10, 1, 5),
            enforce_stationarity=True,
            enforce_invertibility=False,
        )
        joblib.dump(
            loaded_model,
            f"C:\\Users\\ronad\\Downloads\\CryptoPortal\\website\\cryptoportal\\charts\\static\\Models\\{chart}.sav",
        )

    loaded_model = loaded_model.fit()
    forecast = loaded_model.forecast(steps=steps)
    # pred_list = dr + list(forecast)
    # return [str(a) + "\n" for a in pred_list]
    return [str(a) + "\n" for a in forecast]
