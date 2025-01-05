from key import groq_api_key
import sys
import os
from pathlib import Path
from lib.document_classifier import DocumentClassifier

def main():
    # Get API key from environment variable or import from key file

    # Initialize classifier
    base_path = Path("dataroom")
    
    classifier = DocumentClassifier(str(base_path), groq_api_key)

    # Process directory
    dataset_path = Path("dataset")
    results = classifier.process_directory(str(dataset_path))

    # Print results
    #for result in results:
    #   print(f"\nProcessed: {result['file']}")
    #  print(f"Category: {classifier.categories[int(result['classification']['category_id'])]}")
    #    print(f"Confidence: {result['classification']['confidence']}")
    #    print(f"Explanation: {result['classification']['explanation']}")

if __name__ == "__main__":
    main()