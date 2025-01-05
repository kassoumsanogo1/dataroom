import fitz
import docx
from pathlib import Path
from typing import Optional

class DocumentExtractor:
    @staticmethod
    def extract_text_from_pdf(file_path: str, max_pages: int = 20, max_words: int = 10000) -> str:
        """Extrait le texte des premières pages d'un PDF jusqu'à un certain nombre de mots."""
        try:
            doc = fitz.open(file_path)
            text = ""
            for page_num in range(min(max_pages, len(doc))):
                if len(text.split()) >= max_words:
                    break
                text += doc[page_num].get_text()
            doc.close()
            return text
            #return limit_text_length(text, max_words)
        except Exception as e:
            print(f"Erreur lors de la lecture du PDF {file_path}: {str(e)}")
            return ""

    @staticmethod
    def extract_text_from_docx(file_path: str, max_pages: int = 20, max_words: int = 10000) -> str:
        """Extrait le texte des premières pages d'un document Word jusqu'à un certain nombre de mots."""
        try:
            doc = docx.Document(file_path)
            paragraphs_per_page = 3
            max_paragraphs = max_pages * paragraphs_per_page
            text = "\n".join([p.text for p in doc.paragraphs[:max_paragraphs]])
            return text
            #return limit_text_length(text, max_words)
        except Exception as e:
            print(f"Erreur lors de la lecture du document Word {file_path}: {str(e)}")
            return ""