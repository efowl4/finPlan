import customtkinter, sys, os
from PIL import Image, ImageDraw, ImageFont

MAX_LABELS = 23

#Creates location-agnostic filepaths
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        #Exectuable (exists in exec state)
        base_path = sys._MEIPASS
    else:
        #Development
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


#Creates image for Retro Computer font for main menu
custom_font = ImageFont.truetype("../font/Retro_Computer_DEMO.ttf", size=30)
def create_font_image_main(text, x_size, y_size):
    image = Image.new("RGBA", (x_size, y_size), color = (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    draw.text((10,10), text, font=custom_font, fill=(0, 0, 0))
    return customtkinter.CTkImage(light_image=image, dark_image=image, size=(x_size, y_size))

#As above, but changeable size
def create_smallfont_image(text, x_size, y_size):
    image = Image.new("RGBA", (x_size, y_size), color = (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    draw.text((2,2), text, font=custom_font, fill=(0, 0, 0))
    return customtkinter.CTkImage(light_image=image, dark_image=image, size=(x_size, y_size))

def create_label(master, text, row, column):
    new_label = customtkinter.CTkLabel(master,
        text="",
        anchor="w",
        image=create_smallfont_image(text, 450, 40),
        fg_color="#e8e47d")

    new_label.grid(row=row, column=column, sticky="nsew", padx=0, pady=0)
    return new_label

#Creates a new window above main menu
def create_toplevel(master, geometry, title):
    new_top = customtkinter.CTkToplevel(master)
    new_top.geometry(geometry)
    new_top.title(title)
    new_top.focus_force()
    return new_top

#Fills unused column space with empty labels
def fill_column(master, column, starting_row):
    global MAX_LABELS
    remaining_rows = MAX_LABELS - starting_row
    if remaining_rows > 0:
        for i in range(remaining_rows):
            create_label(master, text="", row=(i + starting_row), column=column)
            master.grid_rowconfigure((i + starting_row), weight=0)

#Creates main menu button
def create_button(parent, image_text, command_to_do):
    frame = customtkinter.CTkFrame(master=parent)

    button = customtkinter.CTkButton(master=frame,
        image=image_text,
        text="",
        anchor="nw",
        width=500,
        height=500,
        hover_color="#e64394",
        fg_color="#e8e47d",
        command = command_to_do)
    button.pack(padx=0,pady=0, expand="True", fill="x")
    return frame, button
