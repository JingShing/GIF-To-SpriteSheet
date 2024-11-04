import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageSequence
import os

def select_folder(title):
    folder = filedialog.askdirectory(title=title)
    return folder

def convert_gif_to_spritesheet(source_folder, output_folder, columns=4):
    for filename in os.listdir(source_folder):
        if filename.lower().endswith('.gif'):
            gif_path = os.path.join(source_folder, filename)
            with Image.open(gif_path) as gif:
                frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]
                if frames:
                    frame_width, frame_height = frames[0].size
                    rows = (len(frames) + columns - 1) // columns
                    sheet_width = columns * frame_width
                    sheet_height = rows * frame_height

                    spritesheet = Image.new('RGBA', (sheet_width, sheet_height))

                    for i, frame in enumerate(frames):
                        x = (i % columns) * frame_width
                        y = (i // columns) * frame_height
                        spritesheet.paste(frame, (x, y))

                    output_path = os.path.join(output_folder, filename.replace('.gif', '_spritesheet.png'))
                    spritesheet.save(output_path)
                    print(f"Saved: {output_path}")

# GUI Setup
def main():
    root = tk.Tk()
    root.title("GIF to SpriteSheet Converter")

    source_folder = None
    output_folder = None

    def select_source_folder():
        nonlocal source_folder
        source_folder = select_folder("Select Source Folder")
        if source_folder:
            lbl_source.config(text=f"Source Folder: {source_folder}")

    def select_output_folder():
        nonlocal output_folder
        output_folder = select_folder("Select Output Folder")
        if output_folder:
            lbl_output.config(text=f"Output Folder: {output_folder}")

    def process_conversion():
        columns = entry_columns.get()
        if not columns.isdigit() or int(columns) < 1:
            print("Please enter a valid number of columns.")
            return
        columns = int(columns)

        if not source_folder or not output_folder:
            print("Please make sure all inputs are set.")
            return

        convert_gif_to_spritesheet(source_folder, output_folder, columns)
        print("Conversion completed!")

    tk.Button(root, text="Select Source Folder", command=select_source_folder).pack(pady=5)
    lbl_source = tk.Label(root, text="Source Folder: Not selected")
    lbl_source.pack()

    tk.Button(root, text="Select Output Folder", command=select_output_folder).pack(pady=5)
    lbl_output = tk.Label(root, text="Output Folder: Not selected")
    lbl_output.pack()

    tk.Label(root, text="Enter number of columns:").pack(pady=5)
    entry_columns = tk.Entry(root)
    entry_columns.pack()

    btn_convert = tk.Button(root, text="Start Conversion", command=process_conversion)
    btn_convert.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
