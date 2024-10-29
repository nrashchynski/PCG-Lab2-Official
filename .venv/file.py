from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
#import PIL
from PIL import Image

selected_image_path = ""
diag = 15

def get_folder():
    filepath = filedialog.askdirectory()
    folder_path.delete(0, END)
    folder_path.insert(INSERT, filepath)
    tree.delete(*tree.get_children())
    scan(filepath)

# def get_image():
#     filepath = filedialog.askopenfilename()
#     folder_path.delete(0, END)
#     folder_path.insert(INSERT, os.path.dirname(filepath))
#     tree.delete(*tree.get_children())
#     tree.insert("", END, values=image_info(filepath))
#
# def choose_file_type():
#     file_type = filedialog.askoption(title="Choose File Type", options=["Folder", "Image"])
#     if file_type == "Folder":
#         get_folder()
#     elif file_type == "Image":
#         get_image()path):
    img = Image.open(image_path)
    name = os.path.basename(image_path)
    width, height = img.size
    resolution = (width ** 2 + height ** 2) ** (1 / 2) / diag   #разрешение
    depth = img.mode   #глубина цвета
    compression = img.info.get("compression", "N/A")   #сжатие

    return name, str(width) + 'x' + str(height), resolution, depth, compression,


def scan(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('.jpg', '.gif', '.tif', '.bmp', '.png', '.pcx')):
                tree.insert("", END, values=image_info(os.path.join(root, file)))


def show_image(event):
    global selected_image_path
    selected_item = tree.item(tree.selection())
    image_name = selected_item['values'][0]
    selected_image_path = os.path.join(folder_path.get(), image_name)
    img = Image.open(selected_image_path)
    img.show()


root = Tk()
root.title("Image Info")
root.geometry('600x650')

folder_path = Entry(root, width=40, font=('Arial', 12, 'bold'))
folder_path.grid(row=0, column=0, padx=20, pady=20, sticky=(W, E))
btn_folder_path = Button(root, text="Choose Folder", command=get_folder, width=20,
                         font=('Arial', 12, 'bold'))
btn_folder_path.grid(row=0, column=1, padx=20, pady=20, sticky=(W, E))

columns = ('Name', 'Size', 'Dots/Inch', 'Color Depth', 'Compression')
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.grid(row=1, columnspan=2, sticky=(N, S, W, E))

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", font=('Arial', 12), rowheight=25)
style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))

tree.heading("Name", text="Name")
tree.heading("Size", text="Size")
tree.heading("Dots/Inch", text="Dots/Inch")
tree.heading("Color Depth", text="Color Depth")
tree.heading("Compression", text="Compression")

tree.column("#1", stretch=YES, width=100)
tree.column("#2", stretch=YES, width=100)
tree.column("#3", stretch=YES, width=100)
tree.column("#4", stretch=YES, width=100)
tree.column("#5", stretch=YES, width=100)

scrollbar = ttk.Scrollbar(root, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=1, column=2, sticky=(N, S, W, E))

tree.bind("<<TreeviewSelect>>", show_image)

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
