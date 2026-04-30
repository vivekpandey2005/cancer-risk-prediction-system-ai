import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle

# Sample dataset (you can later replace with real dataset)
data = {
    'age': [25, 45, 50, 35, 60, 30, 55, 40],
    'smoking': [0, 1, 1, 0, 1, 0, 1, 0],
    'family_history': [0, 1, 1, 0, 1, 0, 1, 0],
    'risk': [0, 1, 1, 0, 1, 0, 1, 0]
}

df = pd.DataFrame(data)

X = df[['age', 'smoking', 'family_history']]
y = df['risk']

# Train model
model = LogisticRegression()
model.fit(X, y)

# Save model
pickle.dump(model, open('model.pkl', 'wb'))

print("Model trained and saved!")