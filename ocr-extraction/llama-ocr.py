import requests
import markdown

API_KEY = "635549438045e1155ad195f42776dc103d65500ab999438ce1caffb3391facc9"  # Remplacez par votre clé API Together AI
file_path = "trader-joes-receipt.png"

# Lecture du fichier image
#with open(file_path, "rb") as file:
#    files = {"file": file}

files = {"file": open(file_path, "rb")}  # Ouvrir le fichier sans le fermer immédiatement


# Requête vers l'API Together AI (hypothétique, à ajuster selon la documentation réelle)
response = requests.post(
    "https://api.together.ai/ocr",
    headers={"Authorization": f"Bearer {API_KEY}"},
    files=files,
)

if response.status_code == 200:
    print("Texte extrait :", markdown.response.json()["text"])
else:
    print("Erreur :", response.status_code, response.text)