import concurrent
import requests
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def download_file(url, output_folder):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        filename = url.split('/')[-1]
        file_path = os.path.join(output_folder, filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Laddade ner: {url}")
    except requests.exceptions.RequestException as e:
        print(f"Misslyckades att ladda ner {url}")

def start_download():
    urls = url_text.get(1.0, tk.END).strip().split('\n')
    urls = [url.strip() for url in urls if url.strip()]
    
    if not urls:
        messagebox.showinfo("Info", "Inga URL'er angivna.")
        return
    
    output_folder = folder_path.get()
    if not output_folder:
        messagebox.showinfo("Info", "Välj en output mapp.")
        return
    
    try:
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(download_file, url, output_folder) for url in urls]
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Ett fel har uppstått: {e}")
        messagebox.showinfo("Info", "Alla filer har laddats ner.")
    except Exception as e:
        messagebox.showerror("Fel", f"Ett fel har uppstått")

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)

root = tk.Tk()
root.title("URL Nedladdare")

url_label = tk.Label(root, text="Skriv in URL'er (en per rad):")
url_label.grid(row=0, column=0, padx=5, pady=(25,5))
url_text = tk.Text(root, height=10, width=40)
url_text.grid(row=1, column=0, padx=5, pady=5)

folder_label = tk.Label(root, text="Välj en output mapp:")
folder_label.grid(row=2, column=0, padx=5, pady=(35,5))
folder_path = tk.StringVar()
folder_entry = tk.Entry(root, textvariable=folder_path, width=40)
folder_entry.grid(row=3, column=0, padx=5, pady=5)
select_button = tk.Button(root, text="Välj", command=select_folder)
select_button.grid(row=4, column=0, pady=5)

run_button = tk.Button(root, text="Kör", command=start_download, width=20)
run_button.grid(row=5, column=0, columnspan=2, pady=(35,10))

root.mainloop()