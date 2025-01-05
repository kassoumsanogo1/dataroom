from pathlib import Path
import shutil
from typing import Optional, Dict
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from .file_handler import DocumentExtractor
from .text_processing import TextProcessor

class DocumentClassifier:
    def __init__(self, base_path: str, groq_api_key: str):
        self.base_path = Path(base_path)
        self.categories = {
            1: "contracts",
            2: "personal_documents",
            3: "Food",
            4: "others"
        }
        
        # Création des dossiers
        for category in self.categories.values():
            category_path = self.base_path / category
            category_path.mkdir(parents=True, exist_ok=True)
        
        # Configuration de Groq
        self.llm = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            temperature=0.7,
            api_key=groq_api_key
        )
        
        # Configuration du parser de sortie
        self.response_schemas = [
            ResponseSchema(name="category_id", description="Only The int ID of the category (1-4) corresponding"),
            ResponseSchema(name="confidence", description="Confidence score between 0 and 1"),
            ResponseSchema(name="explanation", description="Brief explanation of the classification")
        ]
        self.output_parser = StructuredOutputParser.from_response_schemas(self.response_schemas)
        
        # Création du prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a document classification expert. Your task is to analyze document content and classify it into one of these categories:

                1: Contracts (Contracts)
                2: Personal Documents (Personal Documents)
                3: Food (Food-related)
                4: Others

                Analyze the content carefully and return:
                1. The category ID int : 1, 2, 3, 4
                2. Your confidence score (0-1)
                3. A brief explanation of your choice

                {format_instructions}"""),
            ("user", "Here is the document content to classify:\n\n{document_content}")
        ])

         # Initialisation du modèle SentenceTransformer
        #self.summary_model = SentenceTransformer('all-MiniLM-L6-v2')

    def classify_text(self, text: str) -> dict:
        """Classifie le texte en utilisant Groq."""
        try:
            if not text.strip():
                return {
                    "category_id": 4,
                    "confidence": 1.0,
                    "explanation": "Document vide"
                }
            
             # Résumer le texte
            summarized_text = TextProcessor.summarize_text(self, text, max_length=1000)

            # Préparation du prompt
            prompt = self.prompt_template.format_messages(
                format_instructions=self.output_parser.get_format_instructions(),
                document_content=summarized_text[:4000]  # Limite de contexte
            )

            # Obtention de la réponse
            response = self.llm.invoke(prompt)
            result = self.output_parser.parse(response.content)
            
            return result

        except Exception as e:
            print(f"Erreur lors de la classification: {str(e)}")
            return {
                "category_id": 4,
                "confidence": 1.0,
                "explanation": "Erreur de classification"
            }

    def process_document(self, file_path: str, max_pages: int = 10, max_words: int = 10000) -> Optional[Dict]:
        """Traite un document et le déplace dans la catégorie appropriée."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                print(f"Le fichier {file_path} n'existe pas.")
                return None

            # Extraction du texte selon le format
            text = ""
            if file_path.suffix.lower() == '.pdf':
                text = DocumentExtractor.extract_text_from_pdf(str(file_path), max_pages=max_pages, max_words=max_words)
            elif file_path.suffix.lower() in ['.docx', '.doc']:
                text = DocumentExtractor.extract_text_from_docx(str(file_path), max_pages=max_pages, max_words=max_words)
            else:
                print(f"Format de fichier non supporté: {file_path.suffix}")
                return None
            
            # Résumé du texte si nécessaire
            #if len(text.split()) > max_summary_words:
            #    text = summarize_text(text, max_summary_words=max_summary_words)

            # Classification du document
            classification_result = self.classify_text(text)
            category_id = int(classification_result['category_id'])
            category = self.categories[category_id]
            
            # Déplacement du fichier
            destination = self.base_path / category / file_path.name

            #pour déplacer
            #shutil.move(str(file_path), str(destination))

            #pour copier
            shutil.copy2(str(file_path), str(destination))
            
            print(f"Document {file_path.name} classé dans la catégorie: {category}")
            print(f"Explication: {classification_result['explanation']}")
            print(f"Confiance: {classification_result['confidence']}")
            
            return classification_result

        except Exception as e:
            print(f"Erreur lors du traitement du document {file_path}: {str(e)}")
            return None

    def process_directory(self, directory_path: str):
        """Processes all documents in a directory."""
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
