import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from config import API_KEY
def fetch_stock_data(symbol, interval='1min'):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={API_KEY}&outputsize=full"
    response = requests.get(url)
    data = response.json()
    time_series = data[f'Time Series ({interval})']
    # Transforming into DataFrame
    df = pd.DataFrame.from_dict(time_series, orient='index', dtype='float')
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)
    data_dict = df.to_dict(orient="index")
    return data_dict

def plot_graph():
    data_dict = fetch_stock_data('AAPL', '1min')
    df = pd.DataFrame.from_dict(data_dict, orient="index", dtype="float")
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)

    fig1, ax1 = plt.subplots(figsize=(7, 5))

    ax1.plot(df.index, df['1. open'], label='Open')
    ax1.plot(df.index, df['2. high'], label='High')
    ax1.plot(df.index, df['3. low'], label='Low')
    ax1.plot(df.index, df['4. close'], label='Close')

    ax1.set_title('Intraday Time Series for AAPL (1min)')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Price')
    ax1.legend()

    fig2, ax2 = plt.subplots(figsize=(7, 5))

    ax2.bar(df.index, df['5. volume'], color='#F39C12')

    ax2.set_title('Trading Volume over Time for AAPL (1min)')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Volume')

    for widget in frame_left.winfo_children():
        widget.destroy()
    for widget in frame_right.winfo_children():
        widget.destroy()

    canvas1 = FigureCanvasTkAgg(fig1, master=frame_left)
    canvas1.draw()
    canvas1.get_tk_widget().pack()

    canvas2 = FigureCanvasTkAgg(fig2, master=frame_right)
    canvas2.draw()
    canvas2.get_tk_widget().pack()

# Creating a Main Window
root = tk.Tk()
root.config(background='#2C3E50')
root.title("Realtime Stock Data Viasualization")
label = tk.Label(root, text='Realtime Stock Data Analytic Dashboard', font=("Raleway",15))
label.pack(padx=30,pady=30)

# Creating Frames for the Plots
frame_left = tk.Frame(root)
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

frame_right = tk.Frame(root)
frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Button to plot graphs
btn_plot = tk.Button(root, text="Generate Plots", command=plot_graph)
btn_plot.config(background='#E74C3C', height=2, width=12)
btn_plot.pack(side=tk.TOP)

# Run the Tkinder event loop
root.mainloop()