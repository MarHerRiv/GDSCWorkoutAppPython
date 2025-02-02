import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk  # Pillow library for image handling
import os
import google.generativeai as genai

class CreateProfilePage:
    def __init__(self, master):
        self.master = master
        master.title("SpaceWorkout")

        self.age_label = ttk.Label(master, text="Age:")
        self.age_label.grid(row=0, column=0, padx=5, pady=10, sticky="w")  # Sticky for left alignment
        self.age_entry = ttk.Entry(master)
        self.age_entry.grid(row=0, column=1, padx=5, pady=10, sticky="ew")  # Sticky for expand

        self.workout_length_label = ttk.Label(master, text="Workout Length (Minutes):")
        self.workout_length_label.grid(row=1, column=0, padx=5, pady=10, sticky="w")
        self.workout_length_entry = ttk.Entry(master)
        self.workout_length_entry.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

        self.workout_duration_label = ttk.Label(master, text="Workout Duration (Days/Week):")
        self.workout_duration_label.grid(row=2, column=0, padx=5, pady=10, sticky="w")
        self.workout_duration_entry = ttk.Entry(master)
        self.workout_duration_entry.grid(row=2, column=1, padx=5, pady=10, sticky="ew")

        self.pic_label = ttk.Label(master)  # Label for the picture
        self.pic_label.grid(row=3, column=0, columnspan=2, padx=5, pady=10)  # Span both columns

        self.upload_pic_button = ttk.Button(master, text="Upload Picture", command=self.upload_picture)
        self.upload_pic_button.grid(row=4, column=0, columnspan=2, pady=(0, 10)) # Span both columns, add top padding

        self.submit_button = ttk.Button(master, text="Submit", command=self.submit_data)
        self.submit_button.grid(row=5, column=0, columnspan=2, pady=(0, 10)) # Span both columns, add top padding

        master.grid_columnconfigure(1, weight=1)  # Make column 1 (entries) expand

        self.image = None  # Store the image object
        self.images = []

    def upload_picture(self):
        file_path = filedialog.askopenfilename(
            title="Select Picture",
            filetypes=(("Image files", "*.jpg;*.jpeg;*.png;*.gif"), ("All files", "*.*"))
        )

        if file_path:
            try:
                image = Image.open(file_path)  # Use PIL to open the image
                image = image.resize((300, 300), Image.LANCZOS)  # Resize image (better quality)
                self.images.append(image)
                self.image = ImageTk.PhotoImage(image) # Store for garbage collection avoidance
                self.pic_label.config(image=self.image)  # Set the image to the label
            except Exception as e:
                messagebox.showerror("Error", f"Error opening image: {e}")

    def submit_data(self):
        age = self.age_entry.get()
        workout_length = self.workout_length_entry.get()
        workout_duration = self.workout_duration_entry.get()
        image_list = self.images

        if not age or not workout_length or not workout_duration or not image_list:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")

            prompt = "Identify the main object in these images. Only respond with one word per object that identifies the object."
            combined_prompt = [prompt]+image_list

            response = model.generate_content(combined_prompt)
            updated_response = (response.text).replace("\n", ", ")

            final_prompt = "Create a workout routine using "+(updated_response)+" as items for a person who is "+age+" and works out for "+workoutlength+" minutes today and "+freq+" days a week. Be concise with your response. It should not exceed 10 lines."
            final_response = model.generate_content(final_prompt)
            
            message = final_response.txt

            messagebox.showinfo("Workout Information", message)


        except ValueError:
            messagebox.showerror("Error", "Invalid input for age, workout length, or duration.")


root = tk.Tk()
create_page = CreateProfilePage(root)
root.mainloop()
