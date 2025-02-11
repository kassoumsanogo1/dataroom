from key import groq_api_key
from pathlib import Path
from lib.document_classifier import DocumentClassifier

def main():

    # Initialize classifier
    base_path = Path("dataroom")
    
    classifier = DocumentClassifier(str(base_path), groq_api_key)

    # Process directory
    dataset_path = Path("dataset")
    results = classifier.process_directory(str(dataset_path))

    #result = classifier.process_document(str(dataset_path))

if __name__ == "__main__":
    main()