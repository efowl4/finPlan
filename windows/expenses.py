from windows.utility import create_smallfont_image, create_label, create_toplevel, fill_column, resource_path
import os.path
import customtkinter
import json

rent = 0.0
food = 0.0
socials = 0.0
other = 0.0
bills = 0.0
total_expenses = 0.0

balance_changes = {}
expense_list = {}

expenses_filepath = resource_path("data/expenses.json")
if os.path.exists(expenses_filepath):
    with open(expenses_filepath, "r") as file:
        expense_list = json.load(file)

def expand_exp(parent):
    window_exp = create_toplevel(parent, "900x900", "Expenses")
    window_exp.grid_rowconfigure(0, weight=1)
    window_exp.grid_columnconfigure(0, weight=1)
    window_exp.grid_columnconfigure(1, weight=1)

    #Configures frames
    grid_frame = customtkinter.CTkFrame(master=window_exp)
    grid_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
    grid_frame.grid_rowconfigure(0, weight=0)
    grid_frame.grid_rowconfigure(1, weight=1)
    grid_frame.grid_columnconfigure(0, weight=1)

    #Unique frame for expense list
    list_frame = customtkinter.CTkFrame(master=grid_frame)
    list_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=10)
    list_frame.grid_columnconfigure(0, weight=1)

    #Button to change expenses
    change_expenses_image = create_smallfont_image("Change Expenses", 450, 40)
    change_expenses_button = customtkinter.CTkButton(
        master=grid_frame,
        text="",
        image=change_expenses_image,
        fg_color="#e8e47d",
        hover_color="#e64394",
        command=lambda: update_expenses(window_exp, list_frame),
    )
    change_expenses_button.grid(row=0, column=0, sticky="ew", padx=0, pady=0)

    #Expense summary
    global total_expenses
    total_expenses = 0
    for row, (name, value) in enumerate(expense_list.items()):
        create_label(list_frame, f"{name}: {value}", row=row + 3, column=0)
        list_frame.grid_rowconfigure(row, weight=0)
        total_expenses += value

    #Total expense cost label
    total_image = create_smallfont_image(f"Total: {total_expenses}", 450, 40)
    display_total_expenses = customtkinter.CTkLabel(
        list_frame, text="", image=total_image, fg_color="#e64394"
    )
    display_total_expenses.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

    #Black space to break up page
    black_space = customtkinter.CTkLabel(master=list_frame, text="", fg_color="black")
    black_space.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)

    fill_column(list_frame, 0, len(expense_list) + 5)

#Creates a window to update expenses and updates the list frame with the new list
def update_expenses(parent, list_frame):
    global expense_list, total_expenses

    change_exp = customtkinter.CTkToplevel(parent)
    change_exp.geometry("400x600")
    change_exp.title("Edit Expenses")
    change_exp.grab_set()

    #Stores new expense costs in a dictionary
    entries = {}

    #Creates a new label for each expense in set out in expense list
    for name, value in expense_list.items():
        label = customtkinter.CTkLabel(change_exp, text=name)
        label.pack(fill="x", padx=10, pady=2)
        entry = customtkinter.CTkEntry(change_exp, font=("Arial", 18), width=200)
        entry.insert(0, str(value))
        entry.pack(fill="x", padx=10, pady=2)
        entries[name] = entry

    def submit():
        global expense_list, total_expenses
        #Update expense_list with new values
        for name, entry in entries.items():
            try:
                cost = float(entry.get())
            except ValueError:
                error_label.config(text="Please enter a number")
            expense_list[name] = cost

        #Overwrite expense values
        with open(expenses_filepath, "w") as file:
            json.dump(expense_list, file, indent=2)

        change_exp.destroy()

        #Update the display in real time - replace widgets with updated ones
        total_expenses = 0
        for widget in list_frame.winfo_children():
            widget.destroy()

        for row, (name, value) in enumerate(expense_list.items()):
            create_label(list_frame, f"{name}: {value}", row=row + 3, column=0)
            list_frame.grid_rowconfigure(row, weight=0)
            total_expenses += value

        total_image = create_smallfont_image(f"Total: {total_expenses}", 450, 40)
        display_total_expenses = customtkinter.CTkLabel(
            list_frame, text="", image=total_image, fg_color="#e8e47d"
        )
        display_total_expenses.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        fill_column(list_frame, 0, (len(expense_list) + 4))

        #Black space to break up page
        black_space = customtkinter.CTkLabel(list_frame, text="", fg_color="black")
        black_space.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)

    error_label = customtkinter.CTkLabel(change_exp, text="")
    error_label.pack()
    submit_btn = customtkinter.CTkButton(change_exp, text="Save", command=submit)
    submit_btn.pack(pady=10)
