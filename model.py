import joblib
import json
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

def train_and_save_model():
    print("Preparing dataset from dataset.json...")
    
    # Load dataset.json
    with open("dataset.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)
        
    # Extract labels and features
    diseases = [item["disease"] for item in dataset]
    # For symptoms, convert the weighted dictionary keys to a list of symptoms
    symptoms = [list(item["symptoms"].keys()) for item in dataset]
    
    # Use MultiLabelBinarizer to convert symptoms list to binary vectors
    mlb = MultiLabelBinarizer()
    X = mlb.fit_transform(symptoms)
    y = np.array(diseases)
    
    print(f"Total samples: {len(X)}")
    print(f"Total features (unique symptoms): {len(mlb.classes_)}")
    print(f"Total unique classes (diseases): {len(set(y))}")
    
    # Use a stratified split to evaluate generalization performance
    # Since we have exactly 10 variations per disease + 15 negative variations,
    # we can do a stratified split (e.g. 80/20 train/test split, meaning 8 training samples and 2 test samples per disease).
    print("Evaluating generalization performance (80/20 stratified split)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train evaluation model
    eval_model = RandomForestClassifier(n_estimators=250, random_state=42, min_samples_split=2)
    eval_model.fit(X_train, y_train)
    y_pred = eval_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Realistic Generalization Accuracy (Clean Test Set): {accuracy * 100:.2f}%")
    
    # Train the final production model on the ENTIRE dataset to maximize learning capacity
    print("Training final production model on the entire dataset...")
    production_model = RandomForestClassifier(n_estimators=250, random_state=42, min_samples_split=2)
    production_model.fit(X, y)
    
    # Save the production model and the encoder
    print("Saving model.pkl and mlb.pkl...")
    joblib.dump(production_model, "model.pkl")
    joblib.dump(mlb, "mlb.pkl")
    print("Done!")

if __name__ == "__main__":
    train_and_save_model()
