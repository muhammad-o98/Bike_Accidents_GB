# src/eda.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure processed folder exists
def ensure_folder(path):
    os.makedirs(path, exist_ok=True)

def accidents_over_time(df: pd.DataFrame, save_path: str = "processed/accidents_over_time.png"):
    """Plot accidents per year and save to file."""
    ensure_folder(os.path.dirname(save_path))
    yearly = df.groupby('year').size()
    plt.figure(figsize=(10,5))
    sns.lineplot(x=yearly.index, y=yearly.values, marker='o')
    plt.title("Number of Bicycle Accidents per Year")
    plt.ylabel("Number of Accidents")
    plt.xlabel("Year")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()  # closes the figure to free memory

def severity_distribution(df: pd.DataFrame, save_path: str = "processed/severity_distribution.png"):
    """Plot severity distribution and save to file."""
    ensure_folder(os.path.dirname(save_path))
    plt.figure(figsize=(6,4))
    sns.countplot(x='severity', data=df, order=['Slight','Serious','Fatal'])
    plt.title("Accident Severity Distribution")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def accidents_by_gender_age(df: pd.DataFrame, save_path: str = "processed/accidents_by_gender_age.png"):
    """Accidents by gender and age group."""
    ensure_folder(os.path.dirname(save_path))
    table = df.groupby(['gender','age_grp']).size().unstack()
    table.plot(kind='bar', stacked=True, figsize=(12,6))
    plt.title("Accidents by Gender and Age Group")
    plt.ylabel("Number of Accidents")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
