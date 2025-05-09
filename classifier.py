import nltk
import pickle
import fitz
from train_model import input_process

def load_artifacts():
    model = pickle.load(open("classifier1.model", 'rb'))
    vectorizer = pickle.load(open("vectorizer1.pickle", 'rb'))
    label_map = pickle.load(open("label_map1.pickle", 'rb'))
    return model, vectorizer, label_map

if __name__ == "__main__":
    nltk.download('stopwords')
    model, vectorizer, label_map = load_artifacts()
    print(label_map)

    path = "testing_mlsvm4.pdf"
    doc = fitz.open(path)

    print("\n--- Document Page-wise Classification ---\n")
    for i in range(len(doc)):
        text = doc[i].get_text()
        cleaned_text = input_process(text)
        vectorized_text = vectorizer.transform([cleaned_text])
        pred = model.predict(vectorized_text)[0]
        # print(pred)
        print(f"Page {i+1}: is about {pred}")
