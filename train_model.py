"""
Train the CSE Placement Readiness model.
Run after generating placement_data.csv.
"""
from pathlib import Path
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "placement_data.csv"
MODEL_PATH = BASE_DIR / "placement_model.pkl"
ENCODER_PATH = BASE_DIR / "label_encoder.pkl"

FEATURE_COLUMNS = [
    "Year", "Coding_Score", "DSA_Score", "Technical_Skills",
    "Projects_Score", "Communication_Score", "Aptitude_Score",
    "Internship_Experience", "Resume_Score"
]
TARGET_COLUMN = "Placement_Readiness"

def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"{DATA_PATH.name} not found. Run: python generate_dataset.py"
        )

    df = pd.read_csv(DATA_PATH)
    missing = [c for c in FEATURE_COLUMNS + [TARGET_COLUMN] if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")

    X = df[FEATURE_COLUMNS].copy()
    y_text = df[TARGET_COLUMN].astype(str)
    encoder = LabelEncoder()
    y = encoder.fit_transform(y_text)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=250, random_state=42, class_weight="balanced"
    )
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    print(f"Test accuracy: {accuracy_score(y_test, predictions):.3f}")
    print("Classes:", list(encoder.classes_))
    print(classification_report(
        y_test, predictions, target_names=encoder.classes_, zero_division=0
    ))

    joblib.dump(model, MODEL_PATH)
    joblib.dump(encoder, ENCODER_PATH)
    print(f"Saved model: {MODEL_PATH.name}")
    print(f"Saved encoder: {ENCODER_PATH.name}")

if __name__ == "__main__":
    main()
