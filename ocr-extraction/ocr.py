import subprocess

def execute_js_script(script_path):
    """
    Exécute le script JavaScript en utilisant Node.js et retourne le résultat.

    :param script_path: Chemin vers le fichier JavaScript à exécuter.
    :return: Une chaîne contenant la sortie standard du script JS ou une erreur.
    """
    try:
        result = subprocess.run(
            ["node", script_path],  # Commande pour exécuter Node.js avec le fichier JS
            #["node", "./ocr-extraction/llama-ocr.js"],  # Commande pour exécuter Node.js avec votre fichier JS
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout  # Retourne la sortie du script JS
    except subprocess.CalledProcessError as e:
        return f"Erreur lors de l'exécution du script JS : {e.stderr}"



# Exemple d'utilisation
script_path = "./ocr-extraction/llama-ocr.js"
resultat = execute_js_script(script_path)
print(resultat)
