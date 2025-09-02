import os.path
import customtkinter
import json

from windows.utility import create_smallfont_image, create_label, create_toplevel, fill_column, resource_path

expected_income_total = 0.0
accrued_income_total = 0.0

income_accrued = {}
income_expected = {}

outstanding_filepath = resource_path("data/income_outstanding.json")
if os.path.exists(outstanding_filepath):
    with open(outstanding_filepath, "r") as file:
        income_accrued = json.load(file)

expected_filepath = resource_path("data/income_expected.json")
if os.path.exists(expected_filepath):
    with open(expected_filepath, "r") as file:
        income_expected = json.load(file)

expected_income_total = round(sum(income_expected.values()), 2)
accrued_income_total = round(sum(income_accrued.values()), 2)

def expand_inc(parent):
    #Income window
    root_inc = create_toplevel(parent, "900x900", "Income")
    root_inc.grid_rowconfigure(0, weight=1)
    root_inc.grid_columnconfigure(0, weight=1)
    root_inc.grid_columnconfigure(1, weight=1)

    #Frames for RHS and LHS, configured for window expansion
    grid_frame_left = customtkinter.CTkFrame(master=root_inc)
    grid_frame_left.grid(row=0, column=0, sticky="nsew", padx=0, pady=1)
    grid_frame_left.grid_rowconfigure(0, weight=0)
    grid_frame_left.grid_columnconfigure(0, weight=1)

    grid_frame_right = customtkinter.CTkFrame(master=root_inc)
    grid_frame_right.grid(row=0, column=1, sticky="nsew", padx=0, pady=1)
    grid_frame_right.grid_rowconfigure(0, weight=0)
    grid_frame_right.grid_columnconfigure(1, weight=1)

    #Labels for totals
    accrued_income_image = create_smallfont_image(f"Total Income: {accrued_income_total}", 450, 40)
    display_accrued_income_total = customtkinter.CTkLabel(grid_frame_left, text="", image=accrued_income_image, fg_color="#e64394")
    display_accrued_income_total.image = accrued_income_image
    display_accrued_income_total.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

    expected_income_image = create_smallfont_image(f"Total Income: {expected_income_total}", 450, 40)
    display_expected_income_total = customtkinter.CTkLabel(grid_frame_right, text="", image=expected_income_image, fg_color="#e64394")
    display_expected_income_total.image = expected_income_image
    display_expected_income_total.grid(row=1, column=1, sticky="nsew", padx=0, pady=0)


    #Frames for income list frames
    expected_list_frame = customtkinter.CTkFrame(master=grid_frame_right)
    expected_list_frame.grid(row=3, column=1, sticky="nsew", padx=0, pady=0)
    expected_list_frame.grid_rowconfigure(0, weight=1)
    expected_list_frame.grid_columnconfigure(0, weight=1)

    accrued_list_frame = customtkinter.CTkFrame(master=grid_frame_left)
    accrued_list_frame.grid(row=3, column=0, sticky="nsew", padx=0, pady=0)
    accrued_list_frame.grid_rowconfigure(0, weight=1)
    accrued_list_frame.grid_columnconfigure(0, weight=1)

    #Updates relevant income and passes the file to update
    def update_income_callback(file_to_write_to):
        getIncome(file_to_write_to)
        refresh_income_lists(expected_list_frame, accrued_list_frame, display_expected_income_total, display_accrued_income_total)

    #Update buttons
    expected_image = create_smallfont_image("Add Expected", 450, 40)
    update_expected_income = customtkinter.CTkButton(
        master=grid_frame_right,
        image=expected_image,
        fg_color="#e8e47d", hover_color="#e64394",
        text="",
        command=lambda: update_income_callback(expected_filepath)
    )
    update_expected_income.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

    accrued_image = create_smallfont_image("Add Accrued", 450, 40)
    update_accrued_income = customtkinter.CTkButton(
        master=grid_frame_left,
        image=accrued_image,
        fg_color="#e8e47d", hover_color="#e64394",
        text="",
        command=lambda: update_income_callback(outstanding_filepath)
    )
    update_accrued_income.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

    #Black labels to break up page
    black_space_left = customtkinter.CTkLabel(grid_frame_left, text="", fg_color="black")
    black_space_left.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)

    black_space_right = customtkinter.CTkLabel(grid_frame_right, text="", fg_color="black")
    black_space_right.grid(row=2, column=1, sticky="nsew", padx=0, pady=0)

    #Initial list frame fill
    refresh_income_lists(expected_list_frame, accrued_list_frame, display_expected_income_total, display_accrued_income_total)


def getIncome(file_to_write_to):
    #Mutable object for modification
    result = {"name": None, "income": None}

    #Obtains name and value of income, stores in file and updates result for return
    def submit():
        value_raw = entry_box_value.get().strip()
        name = entry_box_name.get().strip()

        try:
            value = float(value_raw)
        except ValueError:
            error_label.configure(text="Please enter a number")
            return

        if not name:
            error_label.configure(text="Please enter a name")
            return

        result["name"] = name
        result["income"] = value

        try:
            with open(file_to_write_to, "r") as f:
                store = json.load(f)
            if not isinstance(store, dict):
                store = {}
        except (FileNotFoundError, json.JSONDecodeError):
                store = {}
        store[name] = value

        with open(file_to_write_to, "w") as f:
            json.dump(store, f)

        income_entry.destroy()

    #Update income window
    income_entry = customtkinter.CTk()
    income_entry.geometry("400x400")
    income_entry.title("Update Income")
    income_entry.grab_set()

    entry_box_name = customtkinter.CTkEntry(master=income_entry, font=("Arial", 24), placeholder_text="Enter income name",
                                       width=300, height=70)
    entry_box_name.pack()

    entry_box_value = customtkinter.CTkEntry(master=income_entry, font=("Arial", 24), placeholder_text="Enter a income value",
                                       width=300, height=70)
    entry_box_value.pack()

    error_label = customtkinter.CTkLabel(income_entry, text="")
    error_label.pack()
    income_submit = customtkinter.CTkButton(master=income_entry,command=submit,text="Submit", width=300, height=30)
    income_submit.pack()

    income_entry.wait_window()

    return result

#Refreshes the lists of incomes in the given frames for expected and accrued income
def refresh_income_lists(expected_frame, accrued_frame, display_expected, display_accrued):
    #Destroy labels from previous render
    for widget in expected_frame.winfo_children():
        widget.destroy()
    for widget in accrued_frame.winfo_children():
        widget.destroy()

    #Reloads updated file
    try:
        with open(expected_filepath, "r") as f:
            new_expected = json.load(f)
    except Exception:
        new_expected = {}

    try:
        with open(outstanding_filepath, "r") as f:
            new_accrued = json.load(f)
    except Exception:
        new_accrued = {}

    global expected_income_total, accrued_income_total
    expected_income_total = round(sum(new_expected.values()), 2)
    accrued_income_total = round(sum(new_accrued.values()), 2)

    #Update the totals labels
    new_img_e = create_smallfont_image(f"Total Income: {expected_income_total}", 450, 40)
    display_expected.configure(image=new_img_e)
    display_expected.image = new_img_e

    new_img_a = create_smallfont_image(f"Total Income: {accrued_income_total}", 450, 40)
    display_accrued.configure(image=new_img_a)
    display_accrued.image = new_img_a

    #Render new income lists for expected/accrued
    for i, (key, value) in enumerate(new_expected.items()):
        text = f"{key}: {value}"
        max_length = 15
        if len(text) > max_length:
            max_str = key[:max_length - 3 - len(str(value))]
            text = f"{max_str}... : {value}"

        row_frame = customtkinter.CTkFrame(expected_frame)
        row_frame.grid(row=i+1, column=0, sticky="nsew")
        row_frame.grid_columnconfigure(0, weight=1)
        create_label(row_frame, text=text, row=0, column=0)
        remove_btn_image = create_smallfont_image("X", 40, 40)
        expected_frame.grid_rowconfigure(i, weight=0)

        def make_remove_command(name=key):
            def remove():
                new_expected.pop(name, None)
                with open(expected_filepath, "w") as f:
                    json.dump(new_expected, f)
                refresh_income_lists(expected_frame, accrued_frame, display_expected, display_accrued)
            return remove
        remove_btn = customtkinter.CTkButton(
            master=row_frame, text="", image=remove_btn_image, fg_color="#e64394", hover_color="#e8e47d",
            command=make_remove_command()
        )
        remove_btn.image = remove_btn_image
        remove_btn.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

    fill_column(expected_frame, 0, len(new_expected.keys())+3)

    for i, (key, value) in enumerate(new_accrued.items()):
        text = f"{key}: {value}"
        max_length = 15
        if len(text) > max_length:
            max_str = key[:max_length - 3 - len(str(value))]
            text = f"{max_str}... : {value}"
        row_frame = customtkinter.CTkFrame(accrued_frame)
        row_frame.grid(row=i+1, column=0, sticky="nsew")
        row_frame.grid_columnconfigure(0, weight=1)
        create_label(row_frame, text=text, row=0, column=0)
        remove_btn_image = create_smallfont_image("X", 40, 40)
        accrued_frame.grid_rowconfigure(i, weight=0)

        def make_remove_command(name=key):
            def remove():
                new_accrued.pop(name, None)
                with open(outstanding_filepath, "w") as f:
                    json.dump(new_accrued, f)
                refresh_income_lists(expected_frame, accrued_frame, display_expected, display_accrued)
            return remove

        remove_btn = customtkinter.CTkButton(
            master=row_frame, text="", image=remove_btn_image, fg_color="#e64394", hover_color="#e8e47d",
            command=make_remove_command()
        )
        remove_btn.image = remove_btn_image
        remove_btn.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

    fill_column(accrued_frame, 0, len(new_accrued.keys()) + 3)
