# 📁 Document Classifier with AI-Powered Data Room 🚀

## 📜 Description

Ce projet propose une **Data Room intelligente** qui utilise l'intelligence artificielle pour classifier automatiquement des documents dans des catégories prédéfinies, à partir de leur contenu. Il prend en charge les formats **PDF** et **Word** et inclut les fonctionnalités suivantes :

- 🗂️ Classification automatique des documents dans les catégories :
  - **Contracts** (Contrats)
  - **Personal Documents** (Documents personnels)
  - **Food** (Documents relatifs à l'alimentation)
  - **Others** (Autres documents)
- 🧠 Utilisation d'un modèle NLP avancé pour analyser et classer les documents.
- ✂️ Résumé automatique des documents pour une classification rapide et efficace.
- 📄 Prise en charge des formats **PDF** et **DOCX**.
- 📋 Copie des documents classés dans des sous-dossiers spécifiques (possibilité de déplacer en décommentez une ligne).

## 🛠️ Fonctionnalités

1. **Extraction de texte** 📖 :
   - Lecture des premières pages des documents **PDF** et **Word**.
   - Limitation du texte extrait pour optimiser la classification.

2. **Résumé des documents** ✍️ :
   - Génération d’un résumé des documents longs à l'aide du modèle **SentenceTransformer**.

3. **Classification basée sur l'IA** 🤖 :
   - Utilisation de **Groq AI** pour analyser et classer les documents dans les catégories définies.
   - Score de confiance et explication fournis pour chaque classification.

4. **Gestion automatique des fichiers** 🗃️ :
   - Copie des fichiers classés dans des sous-dossiers correspondant à leur catégorie.

## 🏗️ Architecture

Le projet suit une architecture modulaire composée des éléments suivants :

- **DocumentClassifier** : Classe principale pour gérer l'extraction, la classification, et la copie des documents.
- **Groq AI Integration** : Intégration avec l'API **ChatGroq** pour la classification.
- **SentenceTransformer** : Utilisé pour résumer les documents.

## 🧩 Prérequis

- Python 3.8 ou supérieur 🐍
- Bibliothèques nécessaires (voir [Installation](#installation))
- API Key pour **Groq AI**

## 🚀 Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/kassoumsanogo1/dataroom.git
   ```

2. Installez les dépendances Python :
   ```bash
   pip install -r requirements.txt
   ```

3. Configurez votre clé API Groq dans un fichier Python key.py dans le projet:
   ```python
   groq_api_key = "votre_clé_API"
   ```

4. Créez les dossiers nécessaires pour la Data Room :
   ```bash
   mkdir -p dataroom/contracts dataroom/personal_documents dataroom/Food dataroom/others
   ```

## 🏃‍♂️ Utilisation

1. **Traitement d'un seul document** :
   ```python
   classifier.process_document("chemin/vers/votre/document.pdf")
   ```

2. **Traitement d'un dossier complet** :
   ```python
   classifier.process_directory("chemin/vers/votre/dossier")
   ```

3. **Résultat** :
   - Les documents sont copiés dans les sous-dossiers correspondants :
     ```
     dataroom/
     ├── contracts/
     ├── personal_documents/
     ├── Food/
     └── others/
     ```

## 📦 Dépendances

Voici les bibliothèques nécessaires à ce projet :
- `os`, `pathlib`, `shutil` (Python standard)
- [`PyMuPDF`](https://pypi.org/project/PyMuPDF/) (fitz) pour l'extraction de texte des PDF.
- [`python-docx`](https://pypi.org/project/python-docx/) pour l'extraction de texte des fichiers Word.
- [`langchain`](https://pypi.org/project/langchain/) pour les prompts et l'intégration avec Groq AI.
- [`sentence-transformers`](https://pypi.org/project/sentence-transformers/) pour le résumé automatique des textes.

Installez-les via :
```bash
pip install -r requirements.txt
```

## 📝 Exemple de Résultat

Un exemple de classification d'un document "Contrat" :
```plaintext
Document Tuto-contrat.pdf classé dans la catégorie: contracts
Explication: Ce document contient des termes juridiques relatifs à un contrat.
Confiance: 0.92
```

## 📈 Améliorations futures

- Ajout du support pour d'autres formats de fichiers (Excel, images, etc.) en cours.
- Optimiser le résumé des documents pour inclure des mots-clés pertinents.
- Permettre l'export des résultats sous forme de fichier CSV ou base de données.


## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus d'informations.
