import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import PyPDF2
from googletrans import Translator
from docx import Document
import os

# Bildirim penceresini oluşturmak için işlev
def show_notification(title, message):
    notification_window = tk.Toplevel()
    notification_window.title(title)
    notification_window.geometry("300x100")

    notification_label = tk.Label(notification_window, text=message)
    notification_label.pack()

# tkinter penceresini oluşturun
app = tk.Tk()
app.title("PDF Çevirici")
app.geometry("600x400")

# PDF dosyasını seçme işlevi
def open_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    pdf_file_entry.delete(0, tk.END)
    pdf_file_entry.insert(0, file_path)

pdf_file_label = tk.Label(app, text="PDF Dosyası Seçin:")
pdf_file_label.pack()

pdf_file_entry = tk.Entry(app)
pdf_file_entry.pack()

browse_button = tk.Button(app, text="Gözat", command=open_pdf, width=20, height=2)
browse_button.pack()

# Hedef dosya adı girişi
def set_output_filename():
    file_name = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Files", "*.docx")])
    output_filename_entry.delete(0, tk.END)
    output_filename_entry.insert(0, file_name)

output_filename_label = tk.Label(app, text="Çevrilen Dosya Adı:")
output_filename_label.pack()

output_filename_entry = tk.Entry(app)
output_filename_entry.pack()

output_filename_button = tk.Button(app, text="Dosya Adını Belirle", command=set_output_filename, width=20, height=2)
output_filename_button.pack()

# Çeviri dili seçme işlevi
def select_language():
    selected_language = language_var.get()
    print("Seçilen Dil:", selected_language)

languages = ["az", "en", "fr", "de", "es"]
language_var = tk.StringVar(app)
language_var.set("az")
language_label = tk.Label(app, text="Çeviri Dili Seçin:")
language_label.pack()

language_menu = ttk.Combobox(app, textvariable=language_var, values=languages)
language_menu.pack()

# Çeviri işlemi
def translate_pdf():
    pdf_path = pdf_file_entry.get()
    pdf_file = open(pdf_path, 'rb')

    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    pdf_file.close()

    max_chars = 5000
    text_parts = [text[i:i + max_chars] for i in range(0, len(text), max_chars)]

    translator = Translator()
    translated_text = ""
    target_language = language_var.get()
    for i, part in enumerate(text_parts):
        translation = translator.translate(part, dest=target_language)
        translated_text += translation.text
        if (i + 1) % 5 == 0:
            print(f"{i + 1} bölüm tamamlandı.")
            with open("progress.txt", "w") as progress_file:
                progress_file.write(str(i + 1))
        
        update_progress_bar(i + 1, len(text_parts))

    output_filename = output_filename_entry.get()
    if not output_filename:
        output_filename = "translated_output.docx"

    doc = Document()
    doc.add_paragraph(translated_text)
    doc.save(output_filename)

    # Çeviri işlemi tamamlandığında bildirim gönderin
    show_notification("İşlem Tamamlandı", "PDF çeviri işlemi tamamlandı!")

    # İşlem tamamlandığında dosyayı açma düğmesini etkinleştirin
    open_file_button.config(state=tk.NORMAL)

    # İlerleme çubuğunu sıfırlayın
    progress_bar["value"] = 0

# İlerleme çubuğu ekleyin
progress_bar = ttk.Progressbar(app, length=400, mode='determinate')
progress_bar.pack()

def update_progress_bar(current, total):
    progress = int((current / total) * 100)
    progress_bar["value"] = progress
    app.update_idletasks()

# Dosyayı açmak için işlev
def open_file(file_path):
    os.system(f'start {file_path}')

open_file_button = tk.Button(app, text="Dosyayı Aç", state=tk.DISABLED, command=lambda: open_file(output_filename_entry.get()), width=20, height=2)
open_file_button.pack()

translate_button = tk.Button(app, text="Çevir", command=translate_pdf, width=20, height=2)
translate_button.pack()

app.mainloop()
