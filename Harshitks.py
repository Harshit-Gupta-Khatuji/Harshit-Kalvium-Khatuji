import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Suppress warnings for missing glyphs
warnings.filterwarnings(
    "ignore", message="Glyph .* missing from current font.")

# Load the dataset
df = pd.read_csv('Election-data.csv', encoding='latin1')

# Display the first few rows of the dataset
print("Dataset Preview:")
print(df.head())

# Display column names to check for the presence of 'Gender'
print("\nColumn Names:")
print(df.columns)

# Display information about the dataset
print("\nDataset Information:")
print(df.info())

# Check for duplicated rows
print("\nDuplicated Rows:")
print(df.duplicated().sum())

# Display summary statistics for numerical columns
print("\nSummary Statistics for Numerical Columns:")
print(df.describe())

# Display summary statistics for object columns
print("\nSummary Statistics for Object Columns:")
print(df.describe(include='object'))

# Convert 'Margin' column to numeric, coerce errors to NaN
df['Margin'] = pd.to_numeric(df['Margin'], errors='coerce')

# Check for missing values
print("\nMissing Values:")
print(df.isna().sum())

# Summary statistics for numerical columns
print("\nDetailed Summary Statistics for Numerical Columns:")
print(df.describe())

# Summary statistics for object columns
print("\nDetailed Summary Statistics for Object Columns:")
print(df.describe(include='object'))

# Key Insight 1: Count of Leading Parties
print("\nCount of Leading Parties:")
print(df['Leading Party'].value_counts())

# Key Insight 2: Count of Trailing Parties
print("\nCount of Trailing Parties:")
print(df['Trailing Party'].value_counts())

# Key Insight 3: Status Counts (e.g., Won, Lost)
print("\nStatus Counts:")
print(df['Status'].value_counts())

# Key Insight 4: Distribution of Winning Margins
plt.figure(figsize=(10, 6))
sns.histplot(df['Margin'], bins=30)
plt.title('Distribution of Winning Margins')
plt.xlabel('Margin')
plt.ylabel('Frequency')
plt.show()

# Key Insight 5: Leading Party Count Plot
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='Leading Party',
              order=df['Leading Party'].value_counts().index)
plt.title('Leading Party Count')
plt.xlabel('Party')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.show()

# Key Insight 6: Frequency of Leading Parties by State/UT (Heatmap)
pivot_table = df.pivot_table(
    index='State/UT', columns='Leading Party', aggfunc='size', fill_value=0)
plt.figure(figsize=(10, 8))
sns.heatmap(pivot_table, annot=True, cmap='YlGnBu', fmt='d')
plt.title('Frequency of Leading Parties by State/UT')
plt.xlabel('Leading Party')
plt.ylabel('State/UT')
plt.xticks(rotation=90)
plt.show()

# Key Insight 7: Seat Distribution by Party within Each State (Bar Plot)
plt.figure(figsize=(14, 10))
pivot_table.plot(kind='bar', stacked=True, colormap='tab20', figsize=(15, 10))
plt.title('Seat Distribution by Party within Each State')
plt.xlabel('State/UT')
plt.ylabel('Number of Seats Won')
plt.xticks(rotation=90)
plt.legend(title='Leading Party', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Ensure the 'Gender' column exists before proceeding
if 'Gender' in df.columns:
    # Key Insight 8: Gender Distribution of Elected Representatives
    print("\nGender Distribution of Elected Representatives:")
    print(df['Gender'].value_counts())
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='Gender', order=df['Gender'].value_counts().index)
    plt.title('Gender Distribution of Elected Representatives')
    plt.xlabel('Gender')
    plt.ylabel('Count')
    plt.show()
else:
    print("\nColumn 'Gender' not found in the dataset.")

# Calculate voter turnout percentage
if 'Votes Polled' in df.columns and 'Electors' in df.columns:
    df['Voter Turnout'] = df['Votes Polled'] / df['Electors'] * 100
    # Key Insight 9: Top 10 Constituencies with the Highest Voter Turnout
    top_10_turnout = df.nlargest(10, 'Voter Turnout')
    print("\nTop 10 Constituencies with the Highest Voter Turnout:")
    print(top_10_turnout[['Constituency', 'State/UT', 'Voter Turnout']])

    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_10_turnout, x='Voter Turnout',
                y='Constituency', hue='State/UT')
    plt.title('Top 10 Constituencies with the Highest Voter Turnout')
    plt.xlabel('Voter Turnout (%)')
    plt.ylabel('Constituency')
    plt.show()
else:
    print("\nColumns 'Votes Polled' or 'Electors' not found in the dataset.")

# Key Insight 10: Winning Margin by State
if 'State/UT' in df.columns and 'Margin' in df.columns:
    state_margin = df.groupby(
        'State/UT')['Margin'].mean().sort_values(ascending=False)
    print("\nAverage Winning Margin by State:")
    print(state_margin)

    plt.figure(figsize=(10, 6))
    state_margin.plot(kind='bar')
    plt.title('Average Winning Margin by State')
    plt.xlabel('State/UT')
    plt.ylabel('Average Margin')
    plt.xticks(rotation=90)
    plt.show()
else:
    print("\nColumns 'State/UT' or 'Margin' not found in the dataset.")
