import os
import csv
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import time
import platform
import psutil
import subprocess
import torch
from transformers import Blip2Processor, Blip2ForConditionalGeneration
from PIL import Image
import language_tool_python
from utils import *

#ANCHOR - NLTK-Download
# NLTK-Ressourcen herunterladen
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('words')  # Wortliste hinzufügen

from nltk.corpus import words
english_words_set = set(words.words())

# Funktion zum Überprüfen, ob ein Wort gültig ist
def is_valid_word(word, allowed_words):
    return re.match('^[a-zA-Z]+$', word) and (word.lower() in english_words_set or word.lower() in allowed_words)

#ANCHOR - txt-Files sortieren
# Textdateien sortieren und doppelte Einträge löschen
def remove_duplicates_and_sort(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Eindeutige Zeilen speichern
    unique_lines = set(line.strip().lower() for line in lines if line.strip())

    # Sortierte Liste erstellen
    new_lines = sorted(unique_lines)

    # Schreibe die eindeutigen und sortierten Zeilen zurück in die Datei
    with open(file_path, 'w') as file:
        file.writelines(f"{line}\n" for line in new_lines)

# Funktion zum Laden erlaubter Wörter aus einer Datei
def load_allowed_words(file_path):
    allowed_words = set()
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                word = line.strip().lower()
                if word:  # Fügen Sie nur nicht-leere Wörter hinzu
                    allowed_words.add(word)
    return allowed_words

# Funktion zum Aktualisieren der Ignore-Liste
def update_ignore_list(ignore_list_path, additional_words):
    if os.path.isfile(ignore_list_path):
        with open(ignore_list_path, 'r') as file:
            ignore_words = set(line.strip().lower() for line in file if line.strip())
    else:
        ignore_words = set()

    # Füge neue ungültige Wörter hinzu
    ignore_words.update(additional_words)

    # Überschreibe die Ignore-Liste mit der aktualisierten Version
    with open(ignore_list_path, 'w') as file:
        for word in sorted(ignore_words):
            file.write(word + '\n')

# Bildschirm/Terminal leeren
def clear_screen():
    subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)

# Bildschirm leeren
clear_screen()

#ANCHOR - MPS,Cuda,CPU
# Überprüfen, ob MPS oder CUDA verfügbar ist
device = get_device()
print(f"{'MPS' if device.type == 'mps' else 'CUDA' if device.type == 'cuda' else 'CPU'} wird verwendet\n")

#ANCHOR - Infos
# Programm-Informationen anzeigen
# Hauptprogramm, das auf die externe Datei zugreift
def main():
    print_welcome()
    print_stats()
    print_credits()
    print_footer()

if __name__ == "__main__":
    main()

# Eingabeaufforderung für den Pfad zum Verzeichnis mit den Bildern
standard_image_dir = "/Users/markusrossler/Desktop/Lora/Python"
image_dir = input(f"Bitte geben Sie den Pfad zum Verzeichnis mit den Bildern [{standard_image_dir}]: ") or standard_image_dir

# Eingabeaufforderung für den Pfad zur Ignore-Liste
standard_ignore_list_path = "ignore_liste.txt"
ignore_list_path = input(f"Bitte geben Sie den Pfad zu ignore_liste.txt [{standard_ignore_list_path}]: ") or standard_ignore_list_path

# Eingabeaufforderung für den Pfad zur Datei mit erlaubten Wörtern
standard_allowed_words_path = "allowed_words.txt"  # Standardpfad für erlaubte Wörter
allowed_words_file_path = input(f"Bitte geben Sie den Pfad zur Datei mit erlaubten Wörtern an [{standard_allowed_words_path}]: ") or standard_allowed_words_path

# Sortieren und doppelte Einträge löschen für allowed_words.txt
remove_duplicates_and_sort(allowed_words_file_path)
# Sortieren und doppelte Einträge löschen für ignore_list.txt
remove_duplicates_and_sort(ignore_list_path)

# Laden der erlaubten Wörter
allowed_words = load_allowed_words(allowed_words_file_path)

print(f"Der Pfad zur Ignorieren-Liste ist: {ignore_list_path}")
print(f"Der Pfad zur Ignorieren-Liste ist: {allowed_words_file_path}")

# Bereinigen der Ignore-Liste
if os.path.isfile(ignore_list_path):
    with open(ignore_list_path, 'r') as f:
        ignore_words = set(line.strip().lower() for line in f if line.strip())
else:
    print(f"Die Datei {ignore_list_path} wurde nicht gefunden. Bitte überprüfen Sie den Pfad.")
    exit(1)

# Bereinigen der Allowed-Liste
if os.path.isfile(allowed_words_file_path):
    with open(allowed_words_file_path, 'r') as f:
        allowed_words = set(line.strip().lower() for line in f if line.strip())
else:
    print(f"Die Datei {allowed_words_file_path} wurde nicht gefunden. Bitte überprüfen Sie den Pfad.")
    exit(1)

# Initialisierung von zusätzlichen Wörtern
additional_words = input("Geben Sie 2-3 zusätzliche Wörter ein (durch Kommas getrennt): ")
additional_words = [word.strip().lower() for word in additional_words.split(',') if word.strip()]

gesamt_zeit = time.time()
#ANCHOR - Modelpfad
# Modellpfad
model_path = "/Volumes/SSD T7/Salesforce-blip2-opt-27b" # Local path
#model_path = "Salesforce/blip2-opt-2.7b" # Huggingface path
processor = Blip2Processor.from_pretrained(model_path)
model = Blip2ForConditionalGeneration.from_pretrained(model_path, torch_dtype=torch.float16).to(device)

# Löschen vorhandener Textdateien im Verzeichnis
for filename in os.listdir(image_dir):
    if filename.endswith('.txt'):
        file_path = os.path.join(image_dir, filename)
        os.remove(file_path)
        print(f"Gelöscht: {file_path}")

print("Alle vorhandenen Textdateien wurden gelöscht!")
#ANCHOR - Sprache
# Initialisiere LanguageTool für Englisch
tool = language_tool_python.LanguageTool('en-GB')

# Bildverarbeitung starten
start_zeit = time.time()
for filename in os.listdir(image_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        try:
            image_path = os.path.join(image_dir, filename)
            image = Image.open(image_path).convert("RGB")
            inputs = processor(image, return_tensors="pt").to(device)

            # Generiere Bildbeschreibung
            out = model.generate(**inputs,
                                 do_sample=True,
                                 temperature=1.4,
                                 length_penalty=1.4,
                                 top_k=30,
                                 top_p=0.85,
                                 no_repeat_ngram_size=2,
                                 num_beams=10,
                                 min_length=20,
                                 max_length=80)

            caption = processor.decode(out[0], skip_special_tokens=True).strip()
            caption = ' '.join(caption.split())
            caption = re.sub(r'http\S+|www.\S+', '', caption)

            # Grammatiküberprüfung und Korrektur
            matches = tool.check(caption)
            corrected_caption = language_tool_python.utils.correct(caption, matches)

            # Speichern der Bildbeschreibung in einer Textdatei
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_path = os.path.join(image_dir, txt_filename)
            with open(txt_path, 'w') as txt_file:
                txt_file.write(corrected_caption)
            print(f"Captioned image: {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

##########################

# Verzeichnis mit den Textdateien
text_dir = image_dir
all_extracted_words = []

# Durchlaufen aller Textdateien
for filename in os.listdir(text_dir):
    if filename.endswith('.txt') and filename not in ["gesamt.txt", "extracted_words.txt"]:
        file_path = os.path.join(text_dir, filename)
        with open(file_path, 'r') as file:
            text = file.read()
            # Tokenisieren des Textes
            tokens = word_tokenize(text)
            # POS-Tagging
            tagged_tokens = pos_tag(tokens)
            # Extrahieren der relevanten Wörter
            extracted_words = []
            for token, pos in tagged_tokens:
                if pos in ['NN', 'NNS', 'NNP', 'NNPS', 'VBN', 'RB'] and token.lower() not in ignore_words:
                    extracted_words.append(token)

            # Ungültige Wörter herausfiltern und Ignore-Liste aktualisieren
            invalid_words = [word for word in extracted_words if not is_valid_word(word, allowed_words)]
            new_invalid_words = [word for word in invalid_words if word not in ignore_words]
            update_ignore_list(ignore_list_path, new_invalid_words)

            # Gültige Wörter hinzufügen
            extracted_words = [word for word in extracted_words if is_valid_word(word, allowed_words)]
            combined_words = list(dict.fromkeys(additional_words + extracted_words))  # Kombiniere zusätzliche Wörter und extrahierte Wörter

            # Bildbeschreibung aktualisieren
            with open(file_path, 'w') as file:
                new_description = ", ".join(combined_words) + ", " + text.strip() + ", "
                file.write(new_description)

            all_extracted_words.extend(combined_words)  # Füge die kombinierten Wörter der Liste hinzu
            print(f"Extrahierte Wörter für {filename} wurden hinzugefügt.")

# Entfernen von Duplikaten
all_extracted_words = list(set(all_extracted_words))

# Schreiben der extrahierten Wörter in eine Datei
with open(os.path.join(text_dir, 'extracted_words.txt'), 'w') as file:
    for word in all_extracted_words:
        file.write(word + '\n')

print("Alle extrahierten Wörter wurden in extracted_words.txt gespeichert.")

##########################
# Spezialfunktion: Erstellen einer Textdatei mit allen Beschreibungen und einer CSV-Datei

# Pfad für die Gesamttextdatei und CSV-Datei
gesamt_txt_pfad = os.path.join(image_dir, "gesamt.txt")
csv_pfad = os.path.join(image_dir, "bilderbeschreibungen.csv")

# 1. Alle Textdateien in eine neue "gesamt.txt" einfügen
with open(gesamt_txt_pfad, 'w', encoding='utf-8') as gesamt_file:
    for filename in os.listdir(image_dir):
        if filename.endswith('.txt') and filename not in ["gesamt.txt", "extracted_words.txt"]:
            file_path = os.path.join(image_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()
                gesamt_file.write(content + '\n')  # Jede Beschreibung in einer neuen Zeile

print(f"Alle Beschreibungen wurden in {gesamt_txt_pfad} gespeichert.")

# 2. CSV-Datei mit Bildpfad und Beschreibung erstellen
with open(csv_pfad, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Image Path', 'Description'])  # Header schreiben

    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            bild_pfad = os.path.join(image_dir, filename)  # Vollständigen Pfad verwenden
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_path = os.path.join(image_dir, txt_filename)

            if os.path.exists(txt_path):
                with open(txt_path, 'r', encoding='utf-8') as txt_file:
                    beschreibung = txt_file.read().strip()
                csv_writer.writerow([bild_pfad, beschreibung])

print(f"CSV-Datei mit Bildpfaden und Beschreibungen wurde erstellt in: {csv_pfad}")

##########################
# Tokenizerfunktion: Token-IDs für extrahierte Wörter speichern
with open(os.path.join(text_dir, 't_extracted_words.txt'), 'w', encoding='utf-8') as token_file:
    unique_words = set(all_extracted_words)  # Verwenden Sie ein Set, um Duplikate zu entfernen
    for word in unique_words:
        tokenized_input = processor.tokenizer(word, return_tensors="pt")  # Tokenisierung durchführen
        token_id = tokenized_input['input_ids'][0][1].item()  # Nehmen Sie die Token-ID des ersten Tokens
        token_file.write(f"{word}: {token_id}\n")

print("Tokenizer-Werte wurden in 't_extracted_words.txt' gespeichert.")

""" # Textdateien sortieren und doppelte Einträge löschen
def remove_duplicates_and_sort(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Eindeutige Zeilen speichern
    unique_lines = set(line.strip().lower() for line in lines if line.strip())

    # Sortierte Liste erstellen
    new_lines = sorted(unique_lines)

    # Schreibe die eindeutigen und sortierten Zeilen zurück in die Datei
    with open(file_path, 'w') as file:
        file.writelines(f"{line}\n" for line in new_lines)

# Sortieren und doppelte Einträge löschen für allowed_words.txt
remove_duplicates_and_sort(allowed_words_file_path)
# Sortieren und doppelte Einträge löschen für ignore_list.txt
remove_duplicates_and_sort(ignore_list_path) """

# Beispielaufruf für die Dateien
remove_duplicates_and_sort(os.path.join(text_dir, 't_extracted_words.txt'))
remove_duplicates_and_sort(os.path.join(text_dir, 'extracted_words.txt'))
remove_duplicates_and_sort(os.path.join(text_dir, 'gesamt.txt'))

end_zeit = time.time()
print(f"Nur Textgenerierung und Verarbeitung: {end_zeit - start_zeit:.2f} Sekunden")
print(f"Totale Laufzeit: {end_zeit - gesamt_zeit:.2f} Sekunden")
