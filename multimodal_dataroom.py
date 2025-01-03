import os
from pathlib import Path
import shutil
from typing import List, Optional
from anthropic import Anthropic
import base64

class DocumentClassifier:
    def __init__(self, base_path: str, anthropic_api_key: str):
        self.base_path = Path(base_path)
        self.categories = {
            1: "contrats",
            2: "documents_personnels",
            3: "nourriture",
            4: "others"
        }
        
        # Création des dossiers
        for category in self.categories.values():
            category_path = self.base_path / category
            category_path.mkdir(parents=True, exist_ok=True)
        
        # Configuration du client Anthropic
        self.client = Anthropic(api_key=anthropic_api_key)
        
        self.system_prompt = """You are a document classification expert. Your task is to analyze document content and classify it into one of these categories:

            1: Contrats (Contracts)
            2: Documents Personnels (Personal Documents)
            3: Nourriture (Food-related)
            4: Others

            For each document, provide a JSON response with:
            {
                "category_id": <1-4>,
                "confidence": <0-1>,
                "explanation": "brief explanation"
            }"""

    def encode_file_to_base64(self, file_path: str) -> str:
        """Encode le fichier en base64."""
        with open(file_path, "rb") as file:
            return base64.b64encode(file.read()).decode('utf-8')

    def classify_document(self, file_path: str) -> dict:
        """Classifie le document en utilisant le modèle multimodal."""
        try:
            # Encode le fichier en base64
            file_content = self.encode_file_to_base64(file_path)
            file_ext = Path(file_path).suffix.lower()

            # Détermine le type MIME
            mime_types = {
                '.pdf': 'application/pdf',
                '.doc': 'application/msword',
                '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            }
            mime_type = mime_types.get(file_ext, 'application/octet-stream')

            # Création du message avec le fichier
            message = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                temperature=0.7,
                system=self.system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Please analyze this document and classify it according to the specified categories."
                            },
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": mime_type,
                                    "data": file_content
                                }
                            }
                        ]
                    }
                ]
            )

            # Parse la réponse JSON
            response = eval(message.content[0].text)  # Attention: utilisez json.loads() en production
            return response

        except Exception as e:
            print(f"Erreur lors de la classification: {str(e)}")
            return {
                "category_id": 4,
                "confidence": 1.0,
                "explanation": f"Erreur de classification: {str(e)}"
            }

    def process_document(self, file_path: str) -> Optional[dict]:
        """Traite un document et le déplace dans la catégorie appropriée."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                print(f"Le fichier {file_path} n'existe pas.")
                return None

            if file_path.suffix.lower() not in ['.pdf', '.docx', '.doc']:
                print(f"Format de fichier non supporté: {file_path.suffix}")
                return None

            # Classification du document
            classification_result = self.classify_document(str(file_path))
            category_id = int(classification_result['category_id'])
            category = self.categories[category_id]
            
            # Déplacement du fichier
            destination = self.base_path / category / file_path.name
            shutil.move(str(file_path), str(destination))
            
            print(f"Document {file_path.name} classé dans la catégorie: {category}")
            print(f"Explication: {classification_result['explanation']}")
            print(f"Confiance: {classification_result['confidence']}")
            
            return classification_result

        except Exception as e:
            print(f"Erreur lors du traitement du document {file_path}: {str(e)}")
            return None

    def process_directory(self, directory_path: str):
        """Traite tous les documents dans un répertoire."""
        directory = Path(directory_path)
        results = []
        for file_path in directory.glob("*.*"):
            if file_path.suffix.lower() in ['.pdf', '.docx', '.doc']:
                result = self.process_document(str(file_path))
                if result:
                    results.append({
                        "file": file_path.name,
                        "classification": result
                    })
        return results