import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Similarity:
    def __init__(self):
        pass

    def load_json(self, file_path):
        with open(file_path, 'r') as f:
            return json.load(f)

    def calculate_similarity(self, classJson, outputPath):
        docs = self.load_json(classJson)
        labels = self.load_json('labels.json')
        # Combine all texts to vectorize together for a consistent feature set
        all_texts = list(docs.values()) + list(labels.values())
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(all_texts)
        
        # Split the vectors back into docs and labels parts
        doc_vectors = vectors[:len(docs)]
        label_vectors = vectors[len(docs):]
        
        # Compute cosine similarity between each doc and each label definition
        similarity_scores = cosine_similarity(doc_vectors, label_vectors)

        similarities = {}
        
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
            similarities[doc_key] = {label_key: highestLabel}
        
        with open(outputPath, 'w') as f:
            json.dump(similarities, f)
        return (similarities)

    # Load the JSON data
    def getSimilarities(self, classJson, outputPath):
        return self.calculate_similarity(classJson, outputPath)
