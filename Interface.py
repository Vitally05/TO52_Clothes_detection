import tkinter as tk
from tkinter import filedialog, messagebox, Canvas, NW
from PIL import Image, ImageTk
import Utilities

class App:
    def __init__(self):
        self.selected_image_path = None


def choose_image(app, canvas):
    app.selected_image_path = filedialog.askopenfilename()
    if app.selected_image_path:
        img = Image.open(app.selected_image_path)
        img.thumbnail((150, 150))  # Resize image
        img = ImageTk.PhotoImage(img)
        canvas.create_image(10, 10, anchor=NW, image=img)
        canvas.image = img    # Keep a reference to avoid garbage collection



def select_all(vars):
    for var in vars.values():
        var.set(True)

def deselect_all(vars):
    for var in vars.values():
        var.set(False)

def check_similar_count(similar_count_entry):
    similar_count = get_similar_count(similar_count_entry)
    if similar_count is None:
        return False
    if similar_count < 1 or similar_count > 12:
        messagebox.showerror("Invalid input", "Please enter a number between 1 and 12.")
        return False
    return True

def validate_and_find(similar_count_entry):
    if check_similar_count(similar_count_entry):
        find_items(similar_count_entry)

def get_similar_count(entry):
    try:
        count = int(entry.get())
        return count
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid integer (between 1 and 12) for the number of similar items.")
        return None

def find_items(similar_count_entry):
    similar_count = get_similar_count(similar_count_entry)
    if similar_count is not None:
        print(f"Finding {similar_count} similar items...")
        results(similar_count)

def interface(sizes=["XS", "S", "M", "L", "XL"], brands=["Brand1", "Brand2", "Brand3"]):
    app = App()
    root = tk.Tk()
    root.title("Clothes finder")

    # Image Selection
    image_frame = tk.Frame(root)
    image_frame.pack(pady=10)
    canvas = Canvas(image_frame, width=150, height=150)
    canvas.pack()
    choose_btn = tk.Button(image_frame, text="Choose Image", command=lambda : choose_image(app, canvas))
    choose_btn.pack()


    # Characteristics Section
    char_frame = tk.Frame(root)
    char_frame.pack(pady=10)

    tk.Label(char_frame, text="Size").grid(row=0, column=0, padx=5)

    size_vars = {}
    for i, size in enumerate(sizes):
        var = tk.BooleanVar()
        cb = tk.Checkbutton(char_frame, text=size, variable=var)
        cb.grid(row=i + 1, column=0, sticky='w')
        size_vars[size] = var

    # Button to Select All Sizes
    select_all_btn = tk.Button(char_frame, text="Select All", command=lambda: select_all(size_vars))
    select_all_btn.grid(row=len(sizes) + 1, column=0, pady=5)

    # Button to Deselect All Sizes
    deselect_all_btn = tk.Button(char_frame, text="Deselect All", command=lambda: deselect_all(size_vars))
    deselect_all_btn.grid(row=len(sizes) + 2, column=0, pady=5)

    tk.Label(char_frame, text="Brand").grid(row=0, column=1, padx=5)
    brand_vars = {}
    for i, brand in enumerate(brands):
        var = tk.BooleanVar()
        cb = tk.Checkbutton(char_frame, text=brand, variable=var)
        cb.grid(row=i+1, column=1, sticky='w')
        brand_vars[brand] = var

    # Button to Select All Brands
    select_all_btn = tk.Button(char_frame, text="Select All", command=lambda: select_all(brand_vars))
    select_all_btn.grid(row=len(brands) + 1, column=1, pady=5)

    # Button to Deselect All Brands
    deselect_all_btn = tk.Button(char_frame, text="Deselect All", command=lambda: deselect_all(brand_vars))
    deselect_all_btn.grid(row=len(brands) + 2, column=1, pady=5)

    tk.Label(char_frame, text="How many similar \n (between 1 and 12)").grid(row=0, column=2, padx=5)
    similar_count_entry = tk.Entry(char_frame, width=5)
    similar_count_entry.grid(row=1, column=2, padx=5)
    similar_count_entry.insert(0, "6")  # Default value



    # Find Button
    find_btn = tk.Button(root, text="Find!", command=lambda: validate_and_find(similar_count_entry))
    find_btn.pack(pady=10)

    root.mainloop()

def results(results):
    # Results Area
    root = tk.Tk()
    results_frame = tk.Frame(root)
    results_frame.pack(pady=10)


    # Placeholder for results
    results = int(results)
    results_display_frame = tk.Frame(results_frame)
    results_display_frame.pack(side="left", padx=10)

    for i in range(2):
        for j in range(results // 2):
            result_label = tk.Label(results_display_frame, text="Result", width=30, height=20, borderwidth=1, relief="solid")
            result_label.grid(row=i, column=j, padx=5, pady=5)
            if results % 2 == 1 and i == 0:
                result_label = tk.Label(results_display_frame, text="Result", width=30, height=20, borderwidth=1, relief="solid")
                result_label.grid(row=i, column=j+1, padx=5, pady=5)

    root.mainloop()

if __name__ == '__main__':
    interface()
