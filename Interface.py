import tkinter as tk
from tkinter import filedialog, messagebox, Canvas, NW
from PIL import Image, ImageTk
import Utilities as util

class ClothesFinderApp:
    def __init__(self):
        self.selected_image_path = None
        self.root = tk.Tk()
        self.root.title("Clothes finder")
        self.category = None
        self.brand_vars = {}
        self.size_vars = {}
        self.height = 300
        self.width = 200
        self.canvas = None
        self.similar_count_entry = None



    def create_widgets(self, sizes, brands):
        # Image Selection
        image_frame = tk.Frame(self.root)
        image_frame.pack(pady=10)
        self.canvas = Canvas(image_frame, width=self.width, height=self.height)
        self.canvas.pack()
        choose_btn = tk.Button(image_frame, text="Choose Image", command=self.choose_image)
        choose_btn.pack()

        # Characteristics Section
        char_frame = tk.Frame(self.root)
        char_frame.pack(pady=10)

        tk.Label(char_frame, text="Size").grid(row=0, column=0, padx=5)

        for i, size in enumerate(sizes):
            var = tk.BooleanVar()
            cb = tk.Checkbutton(char_frame, text=size, variable=var)
            cb.grid(row=i + 1, column=0, sticky='w')
            self.size_vars[size] = var

        # Button to Select All Sizes
        select_all_btn = tk.Button(char_frame, text="Select All", command=lambda: self.select_all(self.size_vars))
        select_all_btn.grid(row=len(sizes) + 1, column=0, pady=5)

        # Button to Deselect All Sizes
        deselect_all_btn = tk.Button(char_frame, text="Deselect All", command=lambda: self.deselect_all(self.size_vars))
        deselect_all_btn.grid(row=len(sizes) + 2, column=0, pady=5)

        tk.Label(char_frame, text="Brand").grid(row=0, column=1, padx=5)

        for i, brand in enumerate(brands):
            var = tk.BooleanVar()
            cb = tk.Checkbutton(char_frame, text=brand, variable=var)
            cb.grid(row=i + 1, column=1, sticky='w')
            self.brand_vars[brand] = var

        # Button to Select All Brands
        select_all_btn = tk.Button(char_frame, text="Select All", command=lambda: self.select_all(self.brand_vars))
        select_all_btn.grid(row=len(brands) + 1, column=1, pady=5)

        # Button to Deselect All Brands
        deselect_all_btn = tk.Button(char_frame, text="Deselect All",
                                     command=lambda: self.deselect_all(self.brand_vars))
        deselect_all_btn.grid(row=len(brands) + 2, column=1, pady=5)

        tk.Label(char_frame, text="How many similar \n (between 1 and 12)").grid(row=0, column=2, padx=5)
        self.similar_count_entry = tk.Entry(char_frame, width=5)
        self.similar_count_entry.grid(row=1, column=2, padx=5)
        self.similar_count_entry.insert(0, "6")  # Default value

        # Find Button
        find_btn = tk.Button(self.root, text="Find!", command=self.validate_and_find)
        find_btn.pack(pady=10)

    def get_selected_options(self):
        selected_sizes = [size for size, var in self.size_vars.items() if var.get()]
        selected_brands = [brand for brand, var in self.brand_vars.items() if var.get()]
        return selected_sizes, selected_brands

    def choose_image(self):
        self.selected_image_path = filedialog.askopenfilename()
        if self.selected_image_path:
            img = Image.open(self.selected_image_path)
            img.thumbnail((self.height, self.width))  # Resize image
            img = ImageTk.PhotoImage(img)
            self.canvas.create_image(10, 10, anchor=NW, image=img)
            self.canvas.image = img  # Keep a reference to avoid garbage collection

    def select_all(self, vars):
        for var in vars.values():
            var.set(True)

    def deselect_all(self, vars):
        for var in vars.values():
            var.set(False)

    def get_similar_count(self):
        try:
            count = int(self.similar_count_entry.get())
            return count
        except ValueError:
            messagebox.showerror("Invalid input",
                                 "Please enter a valid integer (between 1 and 12) for the number of similar items.")
            return None

    def check_similar_count(self):
        similar_count = self.get_similar_count()
        if similar_count is None:
            return False
        if similar_count < 1 or similar_count > 12:
            messagebox.showerror("Invalid input", "Please enter a number between 1 and 12.")
            return False
        return True

    def validate_and_find(self):
        if self.check_similar_count():
            similar_count = self.get_similar_count()
            selected_sizes, selected_brands = self.get_selected_options()
            if similar_count is not None:
                print(f"Finding {similar_count} similar items...")
                self.category, bbox = util.predict_category(self.selected_image_path)
                self.selected_image_path = util.crop_image(self.selected_image_path, bbox)
                paths = util.get_images_bdd(self.category, selected_brands, selected_sizes)
                new_paths = util.get_similar_images(paths, self.selected_image_path, similar_count)
                self.show_results(new_paths)

    def show_results(self, results_paths):
        # Results Area
        results_window = tk.Toplevel(self.root)
        results_frame = tk.Frame(results_window)
        results_frame.pack(pady=10)


        # Display the chosen image
        img = Image.open(self.selected_image_path)
        img.thumbnail((self.width, self.height))  # Resize image
        img = ImageTk.PhotoImage(img)
        img_label = tk.Label(results_frame, image=img)
        img_label.image = img  # Keep a reference to avoid garbage collection

        frame = tk.Frame(results_frame)
        frame.pack(side="left", padx=10)

        # Add the image to the frame
        img_label = tk.Label(frame, image=img, width=self.width, height=self.height)
        img_label.pack()

        cat = util.get_category_bdd(self.category)
        category = "Catégorie : " + cat
        # Add the description below the image
        desc_label = tk.Label(frame, text=category, wraplength=self.width, justify="center")
        desc_label.pack()

        # Placeholder for results
        results_display_frame = tk.Frame(results_frame)
        results_display_frame.pack(side="left", padx=10)

        images = []  # List to hold image references to avoid garbage collection

        for index, img_path in enumerate(results_paths):
            img = Image.open(img_path[0])
            img.thumbnail((self.width, self.height))  # Resize image
            img = ImageTk.PhotoImage(img)
            images.append(img)  # Append to the list to keep a reference
            percent = round(img_path[1]*100, 2)
            description = "Taux de similarité : " + str(percent) + "%"

            row = index % 2
            col = index // 2
            # Create a frame for each image and its description
            frame = tk.Frame(results_display_frame, borderwidth=1, relief="solid")
            frame.grid(row=row, column=col, padx=5, pady=5)

            # Add the image to the frame
            img_label = tk.Label(frame, image=img, width=self.width, height=self.height)
            img_label.pack()

            # Add the description below the image
            desc_label = tk.Label(frame, text=description, wraplength=self.width, justify="center")
            desc_label.pack()

        results_window.images = images  # Store the image references in the window to avoid garbage collection

        results_window.mainloop()

    def run(self, sizes, brands):
        self.create_widgets(sizes, brands)
        self.root.mainloop()


if __name__ == '__main__':
    util.clean_destination()
    sizes = util.get_sizes_bdd()
    brands = util.get_brands_bdd()
    app = ClothesFinderApp()
    app.run(sizes=sizes, brands=brands)

