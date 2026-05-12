import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Set up paths
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "roadsense_10k_dataset.csv")

if not os.path.exists(csv_path):
    print(f"Error: {csv_path} not found.")
    exit()

print(f"Loading dataset: {csv_path}")
df = pd.read_csv(csv_path)

# --- THE FIX: Remove any rows with missing data (NaN) ---
initial_count = len(df)
df = df.dropna(subset=['max_jerk', 'target'])
final_count = len(df)
if initial_count > final_count:
    print(f"Cleaned {initial_count - final_count} rows with missing values.")

# Features and Target
X = df[['max_jerk']] 
y = df['target'] 

print("Training RoadSense AI Model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save the trained 'brain'
model_path = os.path.join(base_dir, "pothole_model.pkl")
joblib.dump(model, model_path)
print(f"Success! AI Model saved to {model_path}")
