import pandas as pd
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import string
import nltk
from nltk.corpus import stopwords
import pickle

vectorizer = TfidfVectorizer()
# classification_data.csv
# document_dataset.csv
# df = pd.read_csv('test_dataset_22.csv')
# df=df.isna().sum()
# print(df)
def pre_process_df():
    df = pd.read_csv('test_dataset_22.csv')
    df=df.dropna()
    return df[['text', 'label']]

def input_process(text):
    translator = str.maketrans('', '', string.punctuation)
    nopunc = text.translate(translator)
    words = [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]
    return ' '.join(words)

def remove_stop_words(text_list):
    return [input_process(text) for text in text_list]

def train_model(df):
    X = remove_stop_words(df['text'])
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Train the SVM classifier
    clf = SVC(kernel='linear', probability=True)
    clf.fit(X_train_vec, y_train)

    # save model, vectorizer and class labels
    pickle.dump(clf, open('classifier1.model', 'wb'))
    pickle.dump(vectorizer, open('vectorizer1.pickle', 'wb'))
    pickle.dump(clf.classes_, open('label_map1.pickle', 'wb'))

    print(" model training complete")

    # evaluate the model
    y_pred = clf.predict(X_test_vec)

    # calculate evaluation metrics
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print(f"Accuracy: {accuracy:.4f}")
    print(f"Classification Report:\n{report}")

if __name__ == "__main__":
    nltk.download('stopwords')
    df = pre_process_df()
    train_model(df)
