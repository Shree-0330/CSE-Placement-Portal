import pandas as pd
import numpy as np

# Generate 1000 student records
np.random.seed(42)

n = 1000

data = {
    "Year": np.random.randint(1, 5, n),

    "Coding_Score": np.random.randint(20, 101, n),

    "DSA_Score": np.random.randint(15, 101, n),

    "Technical_Skills": np.random.randint(20, 101, n),

    "Projects_Score": np.random.randint(10, 101, n),

    "Communication_Score": np.random.randint(20, 101, n),

    "Aptitude_Score": np.random.randint(20, 101, n),

    "Internship_Experience": np.random.randint(0, 2, n),

    "Resume_Score": np.random.randint(20, 101, n)
}

# Convert data into DataFrame
df = pd.DataFrame(data)

# Calculate overall placement readiness score
df["Readiness_Score"] = (
    df["Coding_Score"] * 0.15 +
    df["DSA_Score"] * 0.20 +
    df["Technical_Skills"] * 0.15 +
    df["Projects_Score"] * 0.15 +
    df["Communication_Score"] * 0.10 +
    df["Aptitude_Score"] * 0.10 +
    df["Internship_Experience"] * 5 +
    df["Resume_Score"] * 0.10
)

# Convert score into category
def readiness_category(score):

    if score < 45:
        return "Not Ready"

    elif score < 70:
        return "Developing"

    else:
        return "Placement Ready"


df["Placement_Readiness"] = df["Readiness_Score"].apply(
    readiness_category
)

# Save as CSV
df.to_csv("placement_data.csv", index=False)

print("Dataset created successfully!")
print("Shape:", df.shape)
print(df.head())