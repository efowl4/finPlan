import customtkinter

from windows.balance import expand_bal
from windows.income import expand_inc
from windows.expenses import expand_exp
from windows.subscriptions import expand_sub
from windows.utility import create_font_image_main, create_button

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

root_main = customtkinter.CTk()
root_main.geometry("900x900")
root_main.title("FinPlan")
root_main.grid_rowconfigure(0, weight=1)
root_main.grid_rowconfigure(1, weight=4)
root_main.grid_columnconfigure((0,1), weight=1)

image_bal = create_font_image_main("Balance", 350, 60)
image_inc = create_font_image_main("Income", 350, 60)
image_exp = create_font_image_main("Expenses",350, 60)
image_sub = create_font_image_main("Subscriptions",350, 60)

titles = [image_bal, image_inc, image_exp, image_sub]
commands = [
    lambda: expand_bal(root_main),
    lambda: expand_inc(root_main),
    lambda: expand_exp(root_main),
    lambda: expand_sub(root_main)]

for index, label in enumerate(titles):
    row = index // 2
    col = index % 2
    frame, _ = create_button(root_main, titles[index], commands[index])
    frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

root_main.mainloop()