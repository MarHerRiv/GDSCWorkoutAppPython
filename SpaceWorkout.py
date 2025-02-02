import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk  # Pillow library for image handling
import google.generativeai as genai

class CreateSpaceWorkout:
    def __init__(self, master):
        self.master = master
        master.title("SpaceWorkout")

        self.age_label = ttk.Label(master, text="Age:", font="Times 20")
        self.age_label.place(x=20,y=600,width=60)
        self.age_entry = ttk.Entry(master, font="Times 20", width=100)
        self.age_entry.place(x=200,y=600,width=200)

        self.workout_length_label = ttk.Label(master, text="Workout Length", font="Times 16")
        self.workout_length_label.place(x=20,y=675,width=150)
        self.workout_length_2_label = ttk.Label(master, text="(Minutes):", font="Times 16")
        self.workout_length_2_label.place(x=20,y=700,width=125)

        self.workout_length_entry = ttk.Entry(master, font="Times 20", width=100)
        self.workout_length_entry.place(x=200,y=675,width=200)

        #self.workout_duration_label = ttk.Label(master, text="Workout Duration", font="Times 16")
        #self.workout_duration_2_label = ttk.Label(master, text="(Days/Week):", font="Times 16")
        #self.workout_duration_label.place(x=20,y=650,width=200)
        #self.workout_duration_2_label.place(x=20,y=675,width=150)
        #self.workout_duration_entry = ttk.Entry(master, font="Times 20", width=50)
        #self.workout_duration_entry.place(x=200,y=650,width=200)
        
        self.pic_label = ttk.Label(master)  # Label for the picture
        self.pic_label.place(x=25,y=25,width=550,height=550)

        self.extra_pic_label = ttk.Label(master, text="+0", font="Times 32")
        self.extra_pic_label.place(x=600,y=450,width=175,height=175)

        self.upload_pic_button = ttk.Button(master, text="Upload Picture", command=self.upload_picture)
        self.upload_pic_button.place(x=525,y=600,width=200,height=75)

        self.submit_button = ttk.Button(master, text="Submit", command=self.submit_data)
        self.submit_button.place(x=525,y=700,width=200,height=50)

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
                image = image.resize((550, 550), Image.LANCZOS)  # Resize image (better quality)
                self.images.append(image)
                self.image = ImageTk.PhotoImage(image) # Store for garbage collection avoidance
                self.pic_label.config(image=self.image)  # Set the image to the label
                extra_pics = str(len(self.images) - 1)
                self.extra_pic_label.config(text="+"+extra_pics)
                
            except Exception as e:
                messagebox.showerror("Error", f"Error opening image: {e}")

    def submit_data(self):
        age = self.age_entry.get()
        workout_length = self.workout_length_entry.get()
        #workout_duration = self.workout_duration_entry.get()
        image_list = self.images

        if not age or not workout_length or not image_list:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")

            prompt = ("Identify the main object in these images."+
                     " Only respond with one word per object that"+
                     " identifies the object.")
            combined_prompt = [prompt]+image_list

            response = model.generate_content(combined_prompt)
            updated_response = (response.text).replace("\n", ", ")

            """
            final_prompt = ("Create a workout routine using "+
                            (updated_response)+" as items for "+
                            "a person who is "+age+" years old "+
                            "and works out for "+workout_length+
                            " minutes today and "+workout_duration+
                            " days a week. Be concise with your response."+
                            " It should not exceed 10 lines. If one of the"+
                            " items is dangerous, ignore it and proceed with "+
                            "the rest as directed. If an item has absolutely "+
                            "no use for exercise. Ignore it and proceed with the "+
                            "rest as directed.")
            """

            final_prompt = ("Create a workout routine using "+
                            (updated_response)+" as items for "+
                            "a person who is "+age+" years old "+
                            "and works out for "+workout_length+
                            " minutes today. Be concise with your response."+
                            " It should not exceed 10 lines. If one of the"+
                            " items is dangerous, ignore it and proceed with "+
                            "the rest as directed. If an item has absolutely "+
                            "no use for exercise. Ignore it and proceed with the "+
                            "rest as directed.")
            
            final_response = model.generate_content(final_prompt)
            
            message = (final_response).text

            messagebox.showinfo("Workout Information", message)


        except ValueError:
            messagebox.showerror("Error", "Invalid input for age, workout length, or duration.")


root = tk.Tk()
root.geometry("800x800")
root.minsize(800,800)
root.maxsize(800,800)

create_page = CreateSpaceWorkout(root)
root.mainloop()
