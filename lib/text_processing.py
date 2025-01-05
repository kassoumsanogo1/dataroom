from sentence_transformers import SentenceTransformer

class TextProcessor:
    def __init__(self):
        self.summary_model = SentenceTransformer('all-MiniLM-L6-v2')

    def summarize_text(self, text: str, max_length: int = 1000) -> str:
        """Génère un résumé du texte en utilisant SentenceTransformer."""
        try:
            sentences = text.split('. ')
            if len(sentences) <= max_length:
                return text  # Pas de résumé nécessaire

            embeddings = self.summary_model.encode(sentences, convert_to_tensor=True)
            # Classement basé sur les scores d'importance
            scores = embeddings.mean(dim=1).cpu().numpy()
            ranked_sentences = sorted(
                zip(sentences, scores),
                key=lambda x: x[1],
                reverse=True
            )
            summarized = ' '.join([s[0] for s in ranked_sentences[:max_length]])
            return summarized
        except Exception as e:
            print(f"Erreur lors du résumé: {str(e)}")
            return text

    @staticmethod
    def limit_text_length(text: str, max_words: int) -> str:
        """Limits text to a certain number of words."""
        words = text.split()
        if len(words) > max_words:
            return ' '.join(words[:max_words])
        return text