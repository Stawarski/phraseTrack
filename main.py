import tkinter as tk
from tkinter import simpledialog, messagebox, font, Scrollbar, Text
from fetch_data import fetch_page, extract_urls, extract_dialogue_data
from file_operations import write_to_database, search_in_database

def update_dialogues_database():
    try:
        page_x_url = 'https://ben10.fandom.com/wiki/Category:Transcripts'
        base_url = 'https://ben10.fandom.com/wiki/'

        html = fetch_page(page_x_url)
        urls = extract_urls(html, base_url)

        all_data = []

        for url in urls:
            try:
                html = fetch_page(url)
                page_data = extract_dialogue_data(html, url)
                all_data.extend(page_data)
            except Exception as e:
                print(f"Error processing URL {url}: {e}")

        write_to_database(all_data)
        messagebox.showinfo("Update Complete", f"Total lines extracted: {len(all_data)}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update dialogues database: {e}")

def search_in_dialogues_database():
    try:
        string_X = simpledialog.askstring("Input", "Character name:")
        string_Y = simpledialog.askstring("Input", "Phrase:")

        if string_X is not None and string_Y is not None:
            matching_lines = search_in_database(string_X, string_Y)
            if matching_lines:
                show_search_results(matching_lines)
            else:
                messagebox.showinfo("No Matches", "No matching lines found")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to search in dialogues database: {e}")

def show_search_results(lines):
    # Create a new window for displaying search results
    results_window = tk.Toplevel()
    results_window.title("Search Results")
    results_window.geometry("600x400")

    # Define fonts
    bold_font = font.Font(family="Helvetica", size=10, weight="bold")
    normal_font = font.Font(family="Helvetica", size=10)

    # Create a Text widget for displaying results with scrollbar
    text_widget = Text(results_window, wrap="word", font=normal_font)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a Scrollbar and associate it with text_widget
    scrollbar = Scrollbar(results_window, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)

    # Configure tags for different font styles
    text_widget.tag_configure("bold", font=bold_font)
    text_widget.tag_configure("normal", font=normal_font)

    # Insert lines into the Text widget
    for line in lines:
        # Split the line into episode name and dialogue
        parts = line.split(':', 1)
        if len(parts) == 2:
            episode_name = parts[0].strip()
            dialogue = parts[1].strip()

            # Insert episode name in bold and dialogue in normal font using tags
            text_widget.insert(tk.END, f"{episode_name}: ", "bold")
            text_widget.insert(tk.END, f"{dialogue}\n", "normal")

# Create the main window
try:
    root = tk.Tk()
    root.title("PhraseTrack")
    root.geometry("400x200")  # Set the window size to 400x200 pixels

    # Define fonts
    bold_font = font.Font(family="Helvetica", size=12, weight="bold")
    normal_font = font.Font(family="Helvetica", size=10)

    # Create and place the buttons with padding
    btn_update = tk.Button(root, text="Update dialogues database", command=update_dialogues_database, font=normal_font)
    btn_update.pack(pady=20, padx=20)  # Add vertical and horizontal padding

    btn_search = tk.Button(root, text="Search in dialogues database", command=search_in_dialogues_database, font=normal_font)
    btn_search.pack(pady=20, padx=20)  # Add vertical and horizontal padding

    # Run the Tkinter event loop
    root.mainloop()
except Exception as e:
    messagebox.showerror("Error", f"Failed to initialize main window: {e}")