from tkinter import Tk, Label, N, S, E, W, Button, Entry, messagebox, Menu
# from tkinter import *
from zoom_autojoiner_gui.controllers import DatabaseHandler
from zoom_autojoiner_gui.constants import *

# Other fixed constants
# CURRENCY_SYMBOLS = {"INR":"₹", "USD":"$", "GBP":"£", "EUR":"€"}

# Error classes


# Code
portfolio_db_handle = DatabaseHandler() # DB handle
portfolio_gui = Tk() # GUI handle
portfolio_data = CryptoPortfolio(portfolio_db_handle.get_coin_data_to_list(), COINMARKETCAP_API_KEY, API_DOMAIN, CURRENCY_CODE)
def refresh_data():
    return portfolio_data.force_api_update_and_get_portfolio()

def clear_portfolio():
    result = messagebox.askquestion("Warning", "Deleted coins are DELETED FOREVER.\nAre you sure you want to DELETE ALL COINS?")
    if result == "yes":
        portfolio_db_handle.truncate_table()
        portfolio_data.update_portfolio(portfolio_db_handle.get_coin_data_to_list())
        refresh_data_and_write_data_to_tk_window()
        messagebox.showinfo("Information", "Portfolio has been cleared successfully")

def close_app():
    portfolio_gui.destroy()

def write_menu_bar_to_tk_window():
    menu = Menu(portfolio_gui)

    # File menu
    application_item = Menu(menu, tearoff = "off")
    application_item.add_command(label='Clear Portfolio', command=clear_portfolio)
    application_item.add_command(label='Close App', command=close_app)
    menu.add_cascade(label="Application", menu=application_item)
    portfolio_gui.config(menu=menu)

def write_header_to_tk_window(start_at_row = 0):
    # Column Header

    portfolio_id = Label(portfolio_gui, text="Portfolio ID", bg=COLOR_SCHEME["header"]["bg"], fg=COLOR_SCHEME["header"]["fg"], padx=COLOR_SCHEME["header"]["padding"]["x"], pady=COLOR_SCHEME["header"]["padding"]["y"], borderwidth=COLOR_SCHEME["header"]["border"]["width"], relief=COLOR_SCHEME["header"]["border"]["relief"], font=COLOR_SCHEME["header"]["font"]["name"] + " " + COLOR_SCHEME["header"]["font"]["size"] + " " + COLOR_SCHEME["header"]["font"]["style"])
    portfolio_id.grid(row=start_at_row, column=0, sticky=N+S+E+W)

    name = Label(portfolio_gui, text="Coin Name", bg=COLOR_SCHEME["header"]["bg"], fg=COLOR_SCHEME["header"]["fg"], padx=COLOR_SCHEME["header"]["padding"]["x"], pady=COLOR_SCHEME["header"]["padding"]["y"], borderwidth=COLOR_SCHEME["header"]["border"]["width"], relief=COLOR_SCHEME["header"]["border"]["relief"], font=COLOR_SCHEME["header"]["font"]["name"] + " " + COLOR_SCHEME["header"]["font"]["size"] + " " + COLOR_SCHEME["header"]["font"]["style"])
    name.grid(row=start_at_row, column=1, sticky=N+S+E+W)

    price = Label(portfolio_gui, text="Price", bg=COLOR_SCHEME["header"]["bg"], fg=COLOR_SCHEME["header"]["fg"], padx=COLOR_SCHEME["header"]["padding"]["x"], pady=COLOR_SCHEME["header"]["padding"]["y"], borderwidth=COLOR_SCHEME["header"]["border"]["width"], relief=COLOR_SCHEME["header"]["border"]["relief"], font=COLOR_SCHEME["header"]["font"]["name"] + " " + COLOR_SCHEME["header"]["font"]["size"] + " " + COLOR_SCHEME["header"]["font"]["style"])
    price.grid(row=start_at_row, column=2, sticky=N+S+E+W)

    no_coins = Label(portfolio_gui, text="Coin Owned", bg=COLOR_SCHEME["header"]["bg"], fg=COLOR_SCHEME["header"]["fg"], padx=COLOR_SCHEME["header"]["padding"]["x"], pady=COLOR_SCHEME["header"]["padding"]["y"], borderwidth=COLOR_SCHEME["header"]["border"]["width"], relief=COLOR_SCHEME["header"]["border"]["relief"], font=COLOR_SCHEME["header"]["font"]["name"] + " " + COLOR_SCHEME["header"]["font"]["size"] + " " + COLOR_SCHEME["header"]["font"]["style"])
    no_coins.grid(row=start_at_row, column=3, sticky=N+S+E+W)

    tap = Label(portfolio_gui, text="Total Amount Paid", bg=COLOR_SCHEME["header"]["bg"], fg=COLOR_SCHEME["header"]["fg"], padx=COLOR_SCHEME["header"]["padding"]["x"], pady=COLOR_SCHEME["header"]["padding"]["y"], borderwidth=COLOR_SCHEME["header"]["border"]["width"], relief=COLOR_SCHEME["header"]["border"]["relief"], font=COLOR_SCHEME["header"]["font"]["name"] + " " + COLOR_SCHEME["header"]["font"]["size"] + " " + COLOR_SCHEME["header"]["font"]["style"])
    tap.grid(row=start_at_row, column=4, sticky=N+S+E+W)

    curr_val = Label(portfolio_gui, text="Current Value", bg=COLOR_SCHEME["header"]["bg"], fg=COLOR_SCHEME["header"]["fg"], padx=COLOR_SCHEME["header"]["padding"]["x"], pady=COLOR_SCHEME["header"]["padding"]["y"], borderwidth=COLOR_SCHEME["header"]["border"]["width"], relief=COLOR_SCHEME["header"]["border"]["relief"], font=COLOR_SCHEME["header"]["font"]["name"] + " " + COLOR_SCHEME["header"]["font"]["size"] + " " + COLOR_SCHEME["header"]["font"]["style"])
    curr_val.grid(row=start_at_row, column=5, sticky=N+S+E+W)

    plpc = Label(portfolio_gui, text="Profit/Loss per Coin", bg=COLOR_SCHEME["header"]["bg"], fg=COLOR_SCHEME["header"]["fg"], padx=COLOR_SCHEME["header"]["padding"]["x"], pady=COLOR_SCHEME["header"]["padding"]["y"], borderwidth=COLOR_SCHEME["header"]["border"]["width"], relief=COLOR_SCHEME["header"]["border"]["relief"], font=COLOR_SCHEME["header"]["font"]["name"] + " " + COLOR_SCHEME["header"]["font"]["size"] + " " + COLOR_SCHEME["header"]["font"]["style"])
    plpc.grid(row=start_at_row, column=6, sticky=N+S+E+W)

    tplpc = Label(portfolio_gui, text="Total Profit/Loss", bg=COLOR_SCHEME["header"]["bg"], fg=COLOR_SCHEME["header"]["fg"], padx=COLOR_SCHEME["header"]["padding"]["x"], pady=COLOR_SCHEME["header"]["padding"]["y"], borderwidth=COLOR_SCHEME["header"]["border"]["width"], relief=COLOR_SCHEME["header"]["border"]["relief"], font=COLOR_SCHEME["header"]["font"]["name"] + " " + COLOR_SCHEME["header"]["font"]["size"] + " " + COLOR_SCHEME["header"]["font"]["style"])
    tplpc.grid(row=start_at_row, column=7, sticky=N+S+E+W)
    # main_label.pack() # center

    return start_at_row + 1

def write_data_to_tk_window(coin_data, start_at_row = 1):
    i = start_at_row
    for coin in coin_data:
        # Portfolio ID
        lbl = Label(portfolio_gui, text=coin["id"], bg=COLOR_SCHEME["content"]["bg"], fg=COLOR_SCHEME["content"]["fg"], padx=COLOR_SCHEME["content"]["padding"]["x"], pady=COLOR_SCHEME["content"]["padding"]["y"], borderwidth=COLOR_SCHEME["content"]["border"]["width"], relief=COLOR_SCHEME["content"]["border"]["relief"], font=COLOR_SCHEME["content"]["font"]["name"] + " " + COLOR_SCHEME["content"]["font"]["size"] + " " + COLOR_SCHEME["content"]["font"]["style"])
        lbl.grid(row=i, column=0, sticky=N+S+E+W)
        # Coin name
        lbl = Label(portfolio_gui, text=coin["name"] + " (" + coin["symbol"] + ")", bg=COLOR_SCHEME["content"]["bg"], fg=COLOR_SCHEME["content"]["fg"], padx=COLOR_SCHEME["content"]["padding"]["x"], pady=COLOR_SCHEME["content"]["padding"]["y"], borderwidth=COLOR_SCHEME["content"]["border"]["width"], relief=COLOR_SCHEME["content"]["border"]["relief"], font=COLOR_SCHEME["content"]["font"]["name"] + " " + COLOR_SCHEME["content"]["font"]["size"] + " " + COLOR_SCHEME["content"]["font"]["style"])
        lbl.grid(row=i, column=1, sticky=N+S+E+W)
        # Coin price
        coin_price = portfolio_data.get_symbol() + str(coin["price"])
        lbl = Label(portfolio_gui, text=coin_price, bg=COLOR_SCHEME["content"]["bg"], fg=COLOR_SCHEME["content"]["fg"], padx=COLOR_SCHEME["content"]["padding"]["x"], pady=COLOR_SCHEME["content"]["padding"]["y"], borderwidth=COLOR_SCHEME["content"]["border"]["width"], relief=COLOR_SCHEME["content"]["border"]["relief"], font=COLOR_SCHEME["content"]["font"]["name"] + " " + COLOR_SCHEME["content"]["font"]["size"] + " " + COLOR_SCHEME["content"]["font"]["style"])
        lbl.grid(row=i, column=2, sticky=N+S+E+W)
        # No. of coins owned
        lbl = Label(portfolio_gui, text=coin["num_coins_owned"], bg=COLOR_SCHEME["content"]["bg"], fg=COLOR_SCHEME["content"]["fg"], padx=COLOR_SCHEME["content"]["padding"]["x"], pady=COLOR_SCHEME["content"]["padding"]["y"], borderwidth=COLOR_SCHEME["content"]["border"]["width"], relief=COLOR_SCHEME["content"]["border"]["relief"], font=COLOR_SCHEME["content"]["font"]["name"] + " " + COLOR_SCHEME["content"]["font"]["size"] + " " + COLOR_SCHEME["content"]["font"]["style"])
        lbl.grid(row=i, column=3, sticky=N+S+E+W)
        # Total amount paid
        tot_paid = portfolio_data.get_symbol() + str(coin["amount_paid"])
        lbl = Label(portfolio_gui, text=tot_paid, bg=COLOR_SCHEME["content"]["bg"], fg=COLOR_SCHEME["content"]["fg"], padx=COLOR_SCHEME["content"]["padding"]["x"], pady=COLOR_SCHEME["content"]["padding"]["y"], borderwidth=COLOR_SCHEME["content"]["border"]["width"], relief=COLOR_SCHEME["content"]["border"]["relief"], font=COLOR_SCHEME["content"]["font"]["name"] + " " + COLOR_SCHEME["content"]["font"]["size"] + " " + COLOR_SCHEME["content"]["font"]["style"])
        lbl.grid(row=i, column=4, sticky=N+S+E+W)
        # Current market value
        cmv = portfolio_data.get_symbol() + str(coin["current_market_value"])
        lbl = Label(portfolio_gui, text=cmv, bg=COLOR_SCHEME["content"]["bg"], fg=COLOR_SCHEME["content"]["fg"], padx=COLOR_SCHEME["content"]["padding"]["x"], pady=COLOR_SCHEME["content"]["padding"]["y"], borderwidth=COLOR_SCHEME["content"]["border"]["width"], relief=COLOR_SCHEME["content"]["border"]["relief"], font=COLOR_SCHEME["content"]["font"]["name"] + " " + COLOR_SCHEME["content"]["font"]["size"] + " " + COLOR_SCHEME["content"]["font"]["style"])
        lbl.grid(row=i, column=5, sticky=N+S+E+W)
        # Profit/Loss per coin
        if portfolio_data.is_profit(coin["pl_per_coin"]):
            dp_colour = "green"
        else:
            dp_colour = "red"
        plpc = portfolio_data.get_symbol() + str(coin["pl_per_coin"])
        lbl = Label(portfolio_gui, text=plpc, bg=COLOR_SCHEME["content"]["bg"], fg=dp_colour, padx=COLOR_SCHEME["content"]["padding"]["x"], pady=COLOR_SCHEME["content"]["padding"]["y"], borderwidth=COLOR_SCHEME["content"]["border"]["width"], relief=COLOR_SCHEME["content"]["border"]["relief"], font=COLOR_SCHEME["content"]["font"]["name"] + " " + COLOR_SCHEME["content"]["font"]["size"] + " " + COLOR_SCHEME["content"]["font"]["style"])
        lbl.grid(row=i, column=6, sticky=N+S+E+W)
        # Overall profit/loss
        if portfolio_data.is_profit(coin["pl_all_coins"]):
            dp_colour = "green"
        else:
            dp_colour = "red"
        opl = portfolio_data.get_symbol() + str(coin["pl_all_coins"])
        lbl = Label(portfolio_gui, text=opl, bg=COLOR_SCHEME["content"]["bg"], fg=dp_colour, padx=COLOR_SCHEME["content"]["padding"]["x"], pady=COLOR_SCHEME["content"]["padding"]["y"], borderwidth=COLOR_SCHEME["content"]["border"]["width"], relief=COLOR_SCHEME["content"]["border"]["relief"], font=COLOR_SCHEME["content"]["font"]["name"] + " " + COLOR_SCHEME["content"]["font"]["size"] + " " + COLOR_SCHEME["content"]["font"]["style"])
        lbl.grid(row=i, column=7, sticky=N+S+E+W)
        i += 1

    return i

def write_footer_to_tk_window(start_at_row):
    def insert_coin():
        insert_coin_to_db(symbol_txt.get(), amount_txt.get(), price_txt.get())
        refresh_data_and_write_data_to_tk_window()
        messagebox.showinfo("Information", "Coin has been added to portfolio successfully")

    def update_coin():
        update_coin_in_db(upd_id_txt.get(), upd_symbol_txt.get(), upd_amount_txt.get(), upd_price_txt.get())
        refresh_data_and_write_data_to_tk_window()
        messagebox.showinfo("Information", "Coin has been updated successfully")

    def delete_coin():
        result = messagebox.askquestion("Warning", "Deleted coins are DELETED FOREVER.\nAre you sure you want to proceed?")
        if result == "yes":
            delete_coin_in_db(upd_id_txt.get())
            refresh_data_and_write_data_to_tk_window()
            messagebox.showinfo("Information", "Coin has been deleted from portfolio successfully")

    # Total aggregates
    row_no = start_at_row

    lbl = Label(portfolio_gui, text="Total Values:", bg=COLOR_SCHEME["content"]["bg"], fg=COLOR_SCHEME["content"]["fg"], padx=COLOR_SCHEME["content"]["padding"]["x"], pady=COLOR_SCHEME["content"]["padding"]["y"], borderwidth=COLOR_SCHEME["content"]["border"]["width"], relief=COLOR_SCHEME["content"]["border"]["relief"], font=COLOR_SCHEME["content"]["font"]["name"] + " " + COLOR_SCHEME["content"]["font"]["size"] + " " + COLOR_SCHEME["content"]["font"]["style"])
    lbl.grid(row=row_no, column=0, sticky=N+S+E+W)

    lbl = Label(portfolio_gui, text=portfolio_data.get_symbol() + str(round(portfolio_data.get_total_paid_amount(), 2)), bg=COLOR_SCHEME["content"]["bg"], fg=COLOR_SCHEME["content"]["fg"], padx=COLOR_SCHEME["content"]["padding"]["x"], pady=COLOR_SCHEME["content"]["padding"]["y"], borderwidth=COLOR_SCHEME["content"]["border"]["width"], relief=COLOR_SCHEME["content"]["border"]["relief"], font=COLOR_SCHEME["content"]["font"]["name"] + " " + COLOR_SCHEME["content"]["font"]["size"] + " " + COLOR_SCHEME["content"]["font"]["style"])
    lbl.grid(row=row_no, column=4, sticky=N+S+E+W)

    lbl = Label(portfolio_gui, text=portfolio_data.get_symbol() + str(round(portfolio_data.get_total_current_value(), 2)), bg=COLOR_SCHEME["content"]["bg"], fg=COLOR_SCHEME["content"]["fg"], padx=COLOR_SCHEME["content"]["padding"]["x"], pady=COLOR_SCHEME["content"]["padding"]["y"], borderwidth=COLOR_SCHEME["content"]["border"]["width"], relief=COLOR_SCHEME["content"]["border"]["relief"], font=COLOR_SCHEME["content"]["font"]["name"] + " " + COLOR_SCHEME["content"]["font"]["size"] + " " + COLOR_SCHEME["content"]["font"]["style"])
    lbl.grid(row=row_no, column=5, sticky=N+S+E+W)


    if portfolio_data.is_profit(portfolio_data.get_total_pl()):
        dp_colour = "green"
    else:
        dp_colour = "red"

    lbl = Label(portfolio_gui, text=portfolio_data.get_symbol() + str(round(portfolio_data.get_total_pl(), 2)), bg=COLOR_SCHEME["content"]["bg"], fg=dp_colour, padx=COLOR_SCHEME["content"]["padding"]["x"], pady=COLOR_SCHEME["content"]["padding"]["y"], borderwidth=COLOR_SCHEME["content"]["border"]["width"], relief=COLOR_SCHEME["content"]["border"]["relief"], font=COLOR_SCHEME["content"]["font"]["name"] + " " + COLOR_SCHEME["content"]["font"]["size"] + " " + COLOR_SCHEME["content"]["font"]["style"])
    lbl.grid(row=row_no, column=7, sticky=N+S+E+W)

    # Text values and refresh data
    lbl = Label(portfolio_gui, text="Add a coin (refer to headers):", bg=COLOR_SCHEME["content"]["bg"], fg=COLOR_SCHEME["content"]["fg"], padx=COLOR_SCHEME["content"]["padding"]["x"], pady=COLOR_SCHEME["content"]["padding"]["y"], borderwidth=COLOR_SCHEME["content"]["border"]["width"], relief=COLOR_SCHEME["content"]["border"]["relief"], font=COLOR_SCHEME["content"]["font"]["name"] + " " + COLOR_SCHEME["content"]["font"]["size"] + " " + COLOR_SCHEME["content"]["font"]["style"])
    lbl.grid(row=row_no+1, column=0, sticky=N+S+E+W)

    symbol_txt = Entry(portfolio_gui, bg=COLOR_SCHEME["entry"]["bg"], fg=COLOR_SCHEME["entry"]["fg"], borderwidth=COLOR_SCHEME["entry"]["border"]["width"], relief=COLOR_SCHEME["entry"]["border"]["relief"], font=COLOR_SCHEME["entry"]["font"]["name"] + " " + COLOR_SCHEME["entry"]["font"]["size"] + " " + COLOR_SCHEME["entry"]["font"]["style"])
    symbol_txt.grid(row=row_no+1, column=1, sticky=N+S+E+W)

    price_txt = Entry(portfolio_gui, bg=COLOR_SCHEME["entry"]["bg"], fg=COLOR_SCHEME["entry"]["fg"], borderwidth=COLOR_SCHEME["entry"]["border"]["width"], relief=COLOR_SCHEME["entry"]["border"]["relief"], font=COLOR_SCHEME["entry"]["font"]["name"] + " " + COLOR_SCHEME["entry"]["font"]["size"] + " " + COLOR_SCHEME["entry"]["font"]["style"])
    price_txt.grid(row=row_no+1, column=2, sticky=N+S+E+W)

    amount_txt = Entry(portfolio_gui, bg=COLOR_SCHEME["entry"]["bg"], fg=COLOR_SCHEME["entry"]["fg"], borderwidth=COLOR_SCHEME["entry"]["border"]["width"], relief=COLOR_SCHEME["entry"]["border"]["relief"], font=COLOR_SCHEME["entry"]["font"]["name"] + " " + COLOR_SCHEME["entry"]["font"]["size"] + " " + COLOR_SCHEME["entry"]["font"]["style"])
    amount_txt.grid(row=row_no+1, column=3, sticky=N+S+E+W)

    ins_coin_btn = Button(portfolio_gui, text="Add coin", command=insert_coin, bg=COLOR_SCHEME["button"]["bg"], fg=COLOR_SCHEME["button"]["fg"], padx=COLOR_SCHEME["button"]["padding"]["x"], pady=COLOR_SCHEME["button"]["padding"]["y"], borderwidth=COLOR_SCHEME["button"]["border"]["width"], relief=COLOR_SCHEME["button"]["border"]["relief"], font=COLOR_SCHEME["button"]["font"]["name"] + " " + COLOR_SCHEME["button"]["font"]["size"] + " " + COLOR_SCHEME["button"]["font"]["style"])
    ins_coin_btn.grid(row=row_no+1, column=4, sticky=N+S+E+W)

    refresh_btn = Button(portfolio_gui, text="Refresh data", command=refresh_data_and_write_data_to_tk_window, bg=COLOR_SCHEME["button"]["bg"], fg=COLOR_SCHEME["button"]["fg"], padx=COLOR_SCHEME["button"]["padding"]["x"], pady=COLOR_SCHEME["button"]["padding"]["y"], borderwidth=COLOR_SCHEME["button"]["border"]["width"], relief=COLOR_SCHEME["button"]["border"]["relief"], font=COLOR_SCHEME["button"]["font"]["name"] + " " + COLOR_SCHEME["button"]["font"]["size"] + " " + COLOR_SCHEME["button"]["font"]["style"])
    refresh_btn.grid(row=row_no+1, column=7, sticky=N+S+E+W)

    # Update coin
    upd_id_txt = Entry(portfolio_gui, bg=COLOR_SCHEME["entry"]["bg"], fg=COLOR_SCHEME["entry"]["fg"], borderwidth=COLOR_SCHEME["entry"]["border"]["width"], relief=COLOR_SCHEME["entry"]["border"]["relief"], font=COLOR_SCHEME["entry"]["font"]["name"] + " " + COLOR_SCHEME["entry"]["font"]["size"] + " " + COLOR_SCHEME["entry"]["font"]["style"])
    upd_id_txt.grid(row=row_no+2, column=0, sticky=N+S+E+W)

    upd_symbol_txt = Entry(portfolio_gui, bg=COLOR_SCHEME["entry"]["bg"], fg=COLOR_SCHEME["entry"]["fg"], borderwidth=COLOR_SCHEME["entry"]["border"]["width"], relief=COLOR_SCHEME["entry"]["border"]["relief"], font=COLOR_SCHEME["entry"]["font"]["name"] + " " + COLOR_SCHEME["entry"]["font"]["size"] + " " + COLOR_SCHEME["entry"]["font"]["style"])
    upd_symbol_txt.grid(row=row_no+2, column=1, sticky=N+S+E+W)

    upd_price_txt = Entry(portfolio_gui, bg=COLOR_SCHEME["entry"]["bg"], fg=COLOR_SCHEME["entry"]["fg"], borderwidth=COLOR_SCHEME["entry"]["border"]["width"], relief=COLOR_SCHEME["entry"]["border"]["relief"], font=COLOR_SCHEME["entry"]["font"]["name"] + " " + COLOR_SCHEME["entry"]["font"]["size"] + " " + COLOR_SCHEME["entry"]["font"]["style"])
    upd_price_txt.grid(row=row_no+2, column=2, sticky=N+S+E+W)

    upd_amount_txt = Entry(portfolio_gui, bg=COLOR_SCHEME["entry"]["bg"], fg=COLOR_SCHEME["entry"]["fg"], borderwidth=COLOR_SCHEME["entry"]["border"]["width"], relief=COLOR_SCHEME["entry"]["border"]["relief"], font=COLOR_SCHEME["entry"]["font"]["name"] + " " + COLOR_SCHEME["entry"]["font"]["size"] + " " + COLOR_SCHEME["entry"]["font"]["style"])
    upd_amount_txt.grid(row=row_no+2, column=3, sticky=N+S+E+W)

    upd_coin_btn = Button(portfolio_gui, text="Update coin", command=update_coin, bg=COLOR_SCHEME["button"]["bg"], fg=COLOR_SCHEME["button"]["fg"], padx=COLOR_SCHEME["button"]["padding"]["x"], pady=COLOR_SCHEME["button"]["padding"]["y"], borderwidth=COLOR_SCHEME["button"]["border"]["width"], relief=COLOR_SCHEME["button"]["border"]["relief"], font=COLOR_SCHEME["button"]["font"]["name"] + " " + COLOR_SCHEME["button"]["font"]["size"] + " " + COLOR_SCHEME["button"]["font"]["style"])
    upd_coin_btn.grid(row=row_no+2, column=4, sticky=N+S+E+W)

    del_coin_btn = Button(portfolio_gui, text="Delete coin (only id needed)", command=delete_coin, bg=COLOR_SCHEME["button"]["bg"], fg=COLOR_SCHEME["button"]["fg"], padx=COLOR_SCHEME["button"]["padding"]["x"], pady=COLOR_SCHEME["button"]["padding"]["y"], borderwidth=COLOR_SCHEME["button"]["border"]["width"], relief=COLOR_SCHEME["button"]["border"]["relief"], font=COLOR_SCHEME["button"]["font"]["name"] + " " + COLOR_SCHEME["button"]["font"]["size"] + " " + COLOR_SCHEME["button"]["font"]["style"])
    del_coin_btn.grid(row=row_no+2, column=5, sticky=N+S+E+W)

    
def refresh_data_and_write_data_to_tk_window():
    """Destroy frame and recreate it"""    
    for cell in portfolio_gui.winfo_children():
        cell.destroy()
    write_menu_bar_to_tk_window()
    write_footer_to_tk_window(write_data_to_tk_window(refresh_data(), write_header_to_tk_window()))

def insert_coin_to_db(symbol, num_owned, price_per_coin):
    """Insert a coin into Database"""
    portfolio_db_handle.add_coin(symbol, num_owned, price_per_coin)
    portfolio_data.update_portfolio(portfolio_db_handle.get_coin_data_to_list())

def update_coin_in_db(coin_id, symbol, num_owned, price_per_coin):
    """Update coin in Database"""
    portfolio_db_handle.update_coin(coin_id, symbol, num_owned, price_per_coin)
    portfolio_data.update_portfolio(portfolio_db_handle.get_coin_data_to_list())

def delete_coin_in_db(coin_id):
    """Delete coin in Database"""
    portfolio_db_handle.delete_coin(coin_id)
    portfolio_data.update_portfolio(portfolio_db_handle.get_coin_data_to_list())



# Tk
# Widgets
portfolio_gui.title("My Cryptocurrency Portfolio")
portfolio_gui.iconbitmap('Bitcoin-BTC-icon.ico')

# title = Label(portfolio_gui, text="Cryptocurrency Portfolio", bg=COLOR_SCHEME["title"]["bg"], fg=COLOR_SCHEME["title"]["fg"], padx=COLOR_SCHEME["title"]["padding"]["x"], pady=COLOR_SCHEME["title"]["padding"]["y"], borderwidth=COLOR_SCHEME["title"]["border"]["width"], relief=COLOR_SCHEME["title"]["border"]["relief"], font=COLOR_SCHEME["title"]["font"]["name"] + " " + COLOR_SCHEME["title"]["font"]["size"] + " " + COLOR_SCHEME["title"]["font"]["style"])
# title.grid(row=0, column=0)

refresh_data_and_write_data_to_tk_window()

# Show window
portfolio_gui.mainloop() 


