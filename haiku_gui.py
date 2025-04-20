import tkinter as tk
from tkinter import messagebox

#from networkx import generate_gexf
import generate_haiku  # Importing the generate_haiku module

# Create the main app windowx``
app = tk.Tk()
app.title("Haiku Generator")
app.geometry("600x400")

# Add a label
title_label = tk.Label(app, text="Haiku Generator", font=("Helvetica", 18, "bold"))
title_label.pack(pady=10)

# Add an input prompt
prompt_label = tk.Label(app, text="Enter a theme or prompt (optional):", font=("Helvetica", 12))
prompt_label.pack(pady=5)

prompt_entry = tk.Entry(app, font=("Helvetica", 12), width=40)
prompt_entry.pack(pady=5)

# Function for generating full haiku (this will call the function from generate_haiku.py)
def generate_full_haiku_func():
    # Get the user's prompt from the input field
    prompt = prompt_entry.get()  # Assuming `prompt_entry` is the name of the input text field

    if not prompt:
        messagebox.showerror("Error", "Please enter a prompt!")
        return

    # Call the backend function to generate the haiku from generate_haiku.py
    haiku = generate_haiku.generate_full_haiku(prompt)
# If it's not a haiku, display it as-is
    if "Could not generate" in haiku:
            messagebox.showinfo("Generated Text", "Generated text doesn't fit haiku format but here's what was generated:\n" + haiku)
    else:
        messagebox.showinfo("Generated Haiku", haiku)



    # Display the result
    if "Error:" in haiku:
        messagebox.showerror("Error", haiku)
    else:
        messagebox.showinfo("Full Haiku", haiku)

# Placeholder function for collaborative haiku creation
def collaborate_haiku():
    messagebox.showinfo("Collaborative Haiku", "This will start the collaborative haiku creation!")

# Add buttons
generate_button = tk.Button(app, text="Generate Full Haiku", font=("Helvetica", 12), command=generate_full_haiku_func)
generate_button.pack(pady=10)

collaborate_button = tk.Button(app, text="Collaborative Haiku", font=("Helvetica", 12), command=collaborate_haiku)
collaborate_button.pack(pady=10)

# Run the app
app.mainloop()