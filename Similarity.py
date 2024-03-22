import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_json(file_path):
    """Load a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def calculate_similarity(docs, labels):
    """Calculate and print similarity scores between document definitions and label definitions."""
    # Combine all texts to vectorize together for a consistent feature set
    all_texts = list(docs.values()) + list(labels.values())
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(all_texts)
    
    # Split the vectors back into docs and labels parts
    doc_vectors = vectors[:len(docs)]
    label_vectors = vectors[len(docs):]
    
    # Compute cosine similarity between each doc and each label definition
    similarity_scores = cosine_similarity(doc_vectors, label_vectors)
    
    for doc_index, doc_key in enumerate(docs.keys()):
        print(f"--- {doc_key} Similarities ---")
        highestScore = 0
        for label_index, label_key in enumerate(labels.keys()):
            score = similarity_scores[doc_index, label_index]
            if score > highestScore:
                highestScore = score
                highestLabel = label_key
            print(f"{label_key}: {score:.4f}")
        print(f"Most similar label: {highestLabel} : {highestScore:.4f}")
        print()  # Newline for readability between docs

# Load the JSON data
import_docs = load_json('outputs/import_docs.json')
labels = load_json('labels.json')

# Calculate and print the similarity scores
calculate_similarity(import_docs, labels)
