import joblib

model = joblib.load('model.pkl')
mlb = joblib.load('mlb.pkl')

symptoms = ["Difficulty Speaking", "Weakness", "Loss of Balance", "Confusion"]
input_data = mlb.transform([symptoms])

probs = model.predict_proba(input_data)[0]
classes = model.classes_

import numpy as np
top_idx = np.argsort(probs)[::-1][:5]
for i in top_idx:
    print(f"{classes[i]}: {probs[i]*100:.2f}%")
