import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("All_Diets.csv")

# Rename columns (MATCH EXACT CSV NAMES)
df = df.rename(columns={
    "Protein(g)": "Protein",
    "Carbs(g)": "Carbs",
    "Fat(g)": "Fat"
})

print("Columns after rename:", df.columns)

# Handle missing values (numeric only)
df[["Protein", "Carbs", "Fat"]] = df[["Protein", "Carbs", "Fat"]].fillna(
    df[["Protein", "Carbs", "Fat"]].mean()
)

# 1. Average macronutrients per diet type
avg_macros = df.groupby("Diet_type")[["Protein", "Carbs", "Fat"]].mean()
print("\nAverage macronutrients by diet type:\n", avg_macros)

# 2. Top 5 protein-rich recipes per diet type
top_protein = (
    df.sort_values("Protein", ascending=False)
    .groupby("Diet_type")
    .head(5)
)
print("\nTop 5 protein-rich recipes per diet type:\n", top_protein)

# 3. Diet type with highest protein
highest_protein_diet = avg_macros["Protein"].idxmax()
print("\nDiet type with highest average protein:", highest_protein_diet)

# 4. Most common cuisine per diet type
common_cuisines = (
    df.groupby("Diet_type")["Cuisine_type"]
    .agg(lambda x: x.value_counts().idxmax())
)
print("\nMost common cuisine per diet type:\n", common_cuisines)

# 5. New ratio metrics
df["Protein_to_Carbs_ratio"] = df["Protein"] / df["Carbs"]
df["Carbs_to_Fat_ratio"] = df["Carbs"] / df["Fat"]

# VISUALIZATIONS 

# Bar chart
plt.figure(figsize=(10,5))
sns.barplot(x=avg_macros.index, y=avg_macros["Protein"])
plt.title("Average Protein by Diet Type")
plt.xticks(rotation=45)
plt.show()

# Heatmap
plt.figure(figsize=(10,5))
sns.heatmap(avg_macros, annot=True, cmap="coolwarm")
plt.title("Macronutrient Heatmap by Diet Type")
plt.show()

# Scatter plot
plt.figure(figsize=(10,5))
sns.scatterplot(
    data=top_protein,
    x="Protein",
    y="Carbs",
    hue="Cuisine_type"
)
plt.title("Top 5 Protein-Rich Recipes by Cuisine")
plt.show()
