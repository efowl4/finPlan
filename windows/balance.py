import os.path
import customtkinter
import json
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from windows.utility import create_smallfont_image, create_label, create_toplevel, fill_column, resource_path

balance_changes = {}
balance_history = {}

balance_cng_filepath = resource_path("data/balance_changes.json")
if os.path.exists(balance_cng_filepath):
    with open(balance_cng_filepath, "r") as file:
        balance_changes = json.load(file)

balance_upd_filepath = resource_path("data/balance_updates.txt")
if os.path.exists(balance_upd_filepath):
    with open(balance_upd_filepath, "r") as file:
        balance_history = [line.strip() for line in file if line.strip()]

balance = balance_history[-1] if balance_history else 0.0

def expand_bal(parent):
    global balance_changes, balance, balance_history

    window_bal = create_toplevel(parent, "900x900", "Balance")
    window_bal.grid_rowconfigure(0, weight=1)
    window_bal.grid_columnconfigure(0, weight=1)
    window_bal.grid_columnconfigure(1, weight=1)

    frame_left = customtkinter.CTkFrame(master=window_bal)
    frame_left.grid(row=0, column=0, sticky="nsew", padx=0, pady=1)

    frame_right = customtkinter.CTkFrame(master=window_bal)
    frame_right.grid(row=0, column=1, sticky="nsew", padx=0, pady=1)
    frame_right.grid_columnconfigure(1, weight=1)

    num_rows = max(len(balance_changes), 2)

    #LHS
    for i, (key, value) in enumerate(balance_changes.items()):
        text = f"{key}: {value}"
        max_length = 15
        if len(text) > max_length:
            max_str = key[:max_length-3-len(str(value))]
            text = f"{max_str}... : {value}"
        create_label(frame_left, text=text, row=i, column=0)
        frame_left.grid_rowconfigure(i, weight=0)
    frame_left.columnconfigure(0, weight=1)

    fill_column(frame_left, 0, len(balance_changes))

    #Label to show current balance
    balance_text = f"Balance: {balance}"
    balance_image = create_smallfont_image(balance_text, 450, 40)
    balance_display = customtkinter.CTkLabel(master=frame_right, text="", image=balance_image, fg_color="#e64394")
    balance_display.image = balance_image
    balance_display.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

    #Update balance button
    update_button_image = create_smallfont_image("Update Balance", 450, 40)
    update_balance_button = customtkinter.CTkButton(master=frame_right,
        text="",
        image=update_button_image,
        fg_color="#e8e47d",
        hover_color="#e64394",
        corner_radius=0,
        command=lambda: update_balance_callback()
    )
    update_balance_button.grid(row=1, column=1, sticky="ew", padx=0, pady=0)

    #Spacer
    black_space = customtkinter.CTkLabel(master=frame_right, text="", fg_color='black')
    black_space.grid(row=2, column=1, sticky="nsew", padx=0, pady=0)

    #Dedicated frame for the graph
    graph_frame = customtkinter.CTkFrame(master=frame_right)
    graph_frame.grid(row=3, column=1, sticky="nsew", padx=1, pady=1)

    #Initial graph drawing
    draw_balance_graph(graph_frame, balance_history)
    fill_column(frame_right, 1, 19)

    def update_balance_callback():
        global balance, balance_history
        updated_balance = getBalance()
        if updated_balance is not None:
            balance = updated_balance
            #Reload file to dictionary as a single lineZ
            with open(balance_upd_filepath, "r") as file:
                balance_history = [line.strip() for line in file if line.strip()]

            #Update the balance label with new balance total
            new_image = create_smallfont_image(f"Balance: {balance}", 450, 40)
            balance_display.configure(image=new_image)
            balance_display.image = new_image

            #Redraw graph with new balance added, sixth balance removed
            draw_balance_graph(graph_frame, balance_history)

    #Button to change current balance
    update_button_image = create_smallfont_image("Update Balance", 450, 40)
    update_balance_button = customtkinter.CTkButton(master=frame_right,
        text="",
        image=update_button_image,
        fg_color="#e8e47d",
        hover_color="#e64394",
        command=update_balance_callback
    )
    update_balance_button.grid(row=1, column=1, sticky="ew", padx=0, pady=0)

#Creates a window to submit new balance, retrieves new balance
def getBalance():
    #Mutable object for modification
    result = {"balance": None}

    def submit():
        user_balance = entry_box.get()
        if user_balance.replace(".", "", 1).isdigit():
            result["balance"] = float(user_balance)
            #Adds new balance to file
            with open(balance_upd_filepath, "a") as file:
                file.write(str(result["balance"]) + "\n")
            balance_entry.destroy()
        else:
            error_label.configure(text="Please enter a numeric value")

    #New balance entry window
    balance_entry = customtkinter.CTk()
    balance_entry.geometry("400x200")
    balance_entry.title("Update Balance")
    balance_entry.grab_set()

    entry_box = customtkinter.CTkEntry(balance_entry, font=("Arial",24), placeholder_text="Enter your balance", width=300, height=70)
    entry_box.pack()

    error_label = customtkinter.CTkLabel(balance_entry, text="")
    error_label.pack()

    balance_submit = customtkinter.CTkButton(balance_entry, text="Submit", command=submit, width=300, height=30)
    balance_submit.pack()

    balance_entry.wait_window()

    return result["balance"]

#Creates a graph of last 5 balance totals
def draw_balance_graph(graph_frame, balance_history):
    #Remove any existing graph widgets in already the frame
    for widget in graph_frame.winfo_children():
        widget.destroy()
    #Takes last 5 balances from balance history
    last_balances = [float(x) for x in balance_history[-5:]] if balance_history else []
    fig, ax = plt.subplots(figsize=(4, 7.5))
    fig.patch.set_facecolor("#e8e47d")
    if last_balances:
        ax.plot(range(len(last_balances)), last_balances, marker="o", color='black')
        ax.set_title("Balance History")
        ax.set_facecolor("#e64394")
        ax.grid(True)
    else:
        ax.text(0.5, 0.5, "No Data", ha="center", va="center")
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    return canvas
