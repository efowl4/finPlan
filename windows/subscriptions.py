from windows.utility import create_smallfont_image, create_label, create_toplevel, fill_column, resource_path
import os.path
import customtkinter
import json

subscriptions_total = 0.0
subscriptions = {}

subscriptions_filepath = resource_path("data/subscriptions.json")
if os.path.exists(subscriptions_filepath):
    with open(subscriptions_filepath, "r") as file:
        subscriptions = json.load(file)

#Main subscription window - creates top level and initial page structure
def expand_sub(parent):
    root_sub = create_toplevel(parent, "900x900", "Subscriptions")
    root_sub.grid_columnconfigure(0, weight=1)
    root_sub.grid_columnconfigure(1, weight=1)
    root_sub.grid_rowconfigure(0, weight=1)

    list_frame = customtkinter.CTkFrame(master=root_sub, width=450)
    list_frame.grid(row=0, column=0, sticky="nsew")
    list_frame.grid_rowconfigure(0, weight=2)
    list_frame.grid_columnconfigure(0, weight=1)

    frame_right = customtkinter.CTkFrame(master=root_sub, width=450)
    frame_right.grid(row=0, column=1, sticky="nsew")
    frame_right.grid_columnconfigure(1, weight=1)

    update_subscriptions_image = create_smallfont_image("Add Subscription", 450, 40)
    update_subscriptions_button = customtkinter.CTkButton(
        master=frame_right,
        image=update_subscriptions_image,
        text="",
        fg_color="#e8e47d",
        hover_color="#e64394",
        command=lambda: update_subscriptions_dialog(root_sub, list_frame)
    )
    update_subscriptions_button.image = update_subscriptions_image
    update_subscriptions_button.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

    fill_column(frame_right, 1, 1)
    refresh_subscriptions_list(list_frame)

def update_subscriptions_dialog(parent, list_frame):
    dialog = customtkinter.CTkToplevel(parent)
    dialog.geometry("400x300")
    dialog.title("Edit Subscriptions")
    dialog.grab_set()

    name_entry = customtkinter.CTkEntry(dialog, font=("Arial", 18), placeholder_text="Subscription Name", width=200)
    name_entry.pack(pady=10)
    value_entry = customtkinter.CTkEntry(dialog, font=("Arial", 18), placeholder_text="Monthly Cost", width=200)
    value_entry.pack(pady=10)

    def submit():
        name = name_entry.get().strip()
        try:
            value = float(value_entry.get())
        except Exception:
            value = None
            error_label.configure(text="Please enter a numeric value")
            return

        if not name:
            error_label.configure(text="Please enter a name")
            return

        #Save new subscription entry
        try:
            with open(subscriptions_filepath, "r") as f:
                subs = json.load(f)
        except Exception:
            subs = {}
        subs[name] = value
        with open(subscriptions_filepath, "w") as f:
            json.dump(subs, f)
        refresh_subscriptions_list(list_frame)
        dialog.destroy()

    error_label = customtkinter.CTkLabel(dialog, text="", width=200)
    error_label.pack(pady=10)

    submit_btn = customtkinter.CTkButton(dialog, text="Save", command=submit)
    submit_btn.pack(pady=10)

def refresh_subscriptions_list(list_frame):
    #Clear old widgets
    for widget in list_frame.winfo_children():
        widget.destroy()
    try:
        with open(subscriptions_filepath, "r") as f:
            subs = json.load(f)
    except Exception:
        subs = {}

    #Total label
    total_image = create_smallfont_image(f"Total: {round(sum(subs.values()), 2)}", 450, 40)
    total = customtkinter.CTkLabel(list_frame, text="", image=total_image, fg_color="#e64394")
    total.image = total_image
    total.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

    for i, (key, value) in enumerate(subs.items()):
        text = f"{key}: {value}"
        max_length = 15
        if len(text) > max_length:
            max_str = key[:max_length - 3 - len(str(value))]
            text = f"{max_str}... : {value}"
        row_frame = customtkinter.CTkFrame(list_frame)
        row_frame.grid(row=i+1, column=0, sticky="nsew")
        row_frame.grid_columnconfigure(0, weight=1)
        create_label(row_frame, text=text, row=0, column=0)
        remove_btn_image = create_smallfont_image("X", 40, 40)
        list_frame.grid_rowconfigure(i, weight=0)

        def make_remove_command(name=key):
            def remove():
                subs.pop(name, None)
                with open(subscriptions_filepath, "w") as f:
                    json.dump(subs, f)
                refresh_subscriptions_list(list_frame)
            return remove
        remove_btn = customtkinter.CTkButton(
            row_frame, text="", image=remove_btn_image, fg_color="#e64394", hover_color="#e8e47d",
            command=make_remove_command()
        )
        remove_btn.image = remove_btn_image
        remove_btn.grid(row=0, column=1, sticky="nsew")

    fill_column(list_frame, 0, len(subs)+2)
