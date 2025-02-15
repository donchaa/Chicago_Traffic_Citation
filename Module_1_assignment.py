#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display  # For displaying tables in Jupyter Notebook

# Load the dataset
file_path = "Chicago Traffic Citations.csv"
df = pd.read_csv(file_path)

# --- DATASET OVERVIEW ---
print("\nDataset Overview:")
display(df.info())  # Shows basic information about the dataset

# Display first few rows in a readable format
print("\nSample Data:")
display(df.head())

# Convert 'Issue Date' to datetime format
df['Issue Date'] = pd.to_datetime(df['Issue Date'], errors='coerce')

# Drop duplicates and handle missing values
df.drop_duplicates(inplace=True)
df.fillna({'Violation Location': 'Unknown', 'Zip Code': 'Unknown', 'Vehicle Make': 'Unknown'}, inplace=True)
df.fillna(0, inplace=True)

# Sort data by Issue Date (most recent first)
df.sort_values(by="Issue Date", ascending=False, inplace=True)

# Save cleaned data
df.to_csv("Cleaned_Chicago_Traffic_Citations.csv", index=False)

# --- DATA ANALYSIS ---

# Top 10 most frequent violations
top_violations = df['Violation Description'].value_counts().head(10).reset_index()
top_violations.columns = ['Violation Description', 'Number of Citations']

# Top 10 violation locations
top_locations = df['Violation Location'].value_counts().head(10).reset_index()
top_locations.columns = ['Violation Location', 'Number of Citations']

# Violations at top locations
df_top_locations = df[df['Violation Location'].isin(top_locations['Violation Location'])]

# Count the most common violations at each location
violation_counts = df_top_locations.groupby(['Violation Location', 'Violation Description']).size().reset_index(name='Count')

# Pivot data for top 3 violations per location
top_violations_per_location = violation_counts.groupby('Violation Location').apply(lambda x: x.nlargest(3, 'Count')).reset_index(drop=True)
pivot_table = top_violations_per_location.pivot(index='Violation Location', columns='Violation Description', values='Count').fillna(0).astype(int)

# --- DISPLAY TABLES AND VISUALIZATIONS ---

# Display dataset overview again for clarity
print("\nCleaned Dataset Overview:")
display(df.info())

# Display top violations table
print("\nTop 10 Most Frequent Traffic Violations in Chicago:\n")
display(top_violations)

# Plot top violations
plt.figure(figsize=(12, 6))
sns.barplot(x=top_violations['Violation Description'], y=top_violations['Number of Citations'], hue=top_violations['Violation Description'], legend=False, palette="Blues_r")
plt.xticks(rotation=45, ha="right")
plt.title("Top 10 Most Frequent Traffic Violations in Chicago")
plt.xlabel("Violation Type")
plt.ylabel("Number of Citations")
plt.show()

# Display top ticketed locations table
print("\nTop 10 Locations with the Most Traffic Citations in Chicago:\n")
display(top_locations)

# Plot most ticketed locations
plt.figure(figsize=(12, 6))
sns.barplot(x=top_locations['Violation Location'], y=top_locations['Number of Citations'], hue=top_locations['Violation Location'], legend=False, palette="Reds_r")
plt.xticks(rotation=45, ha="right")
plt.title("Top 10 Locations with the Most Traffic Citations in Chicago")
plt.xlabel("Violation Location")
plt.ylabel("Number of Citations")
plt.show()

# Display violations per location table
print("\nTop 3 Violations at the Most Ticketed Locations in Chicago:\n")
display(pivot_table)

# Stacked bar chart for violations at top locations
plt.figure(figsize=(14, 7))
pivot_table.plot(kind='bar', stacked=True, colormap='viridis', figsize=(14,7))
plt.title("Most Common Violations at Top 10 Ticketed Locations in Chicago")
plt.xlabel("Violation Location")
plt.ylabel("Number of Citations")
plt.xticks(rotation=45, ha="right")
plt.legend(title="Violation Type", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


# In[ ]:




