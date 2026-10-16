#!/usr/bin/env python3
"""
visualize.py
------------
Project: Netflix Movies and TV Shows Data Analysis using Hadoop and Hive
Purpose: Generates clean, publication-ready analytical charts and a unified dashboard
         from HiveQL query result CSVs stored in results/data/.

Usage:
    python visualize.py
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Setup paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "results", "data")
CHARTS_DIR = os.path.join(PROJECT_ROOT, "results", "charts")

os.makedirs(CHARTS_DIR, exist_ok=True)

# Visual styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
NETFLIX_RED = '#E50914'
NETFLIX_BLACK = '#221F1F'
NETFLIX_DARK = '#141414'
ACCENT_GRAY = '#737373'
ACCENT_BLUE = '#0071EB'
PALETTE = ['#E50914', '#221F1F', '#B81D24', '#564D4D', '#831010', '#4B6B94', '#6D98BA', '#2E4057']

def plot_content_type():
    """Chart 1: Movies vs TV Shows Distribution (Donut Chart)"""
    csv_path = os.path.join(DATA_DIR, "q1_content_type_distribution.csv")
    if not os.path.exists(csv_path):
        print(f"[-] Missing: {csv_path}")
        return
    df = pd.read_csv(csv_path)

    fig, ax = plt.subplots(figsize=(7, 6))
    colors = [NETFLIX_RED, '#333333']
    wedges, texts, autotexts = ax.pie(
        df['count'],
        labels=df['type'],
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        textprops={'fontsize': 12, 'weight': 'bold'},
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2)
    )
    for at in autotexts:
        at.set_color('white')
        at.set_fontsize(13)

    plt.title("Netflix Catalog Breakdown: Movies vs TV Shows\n(Total: 6,234 Titles)", fontsize=14, weight='bold', pad=15)
    plt.tight_layout()
    output_path = os.path.join(CHARTS_DIR, "01_movies_vs_tv_shows.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[+] Generated: {output_path}")

def plot_releases_by_year():
    """Chart 2: Content Output by Release Year (Line/Area Chart)"""
    csv_path = os.path.join(DATA_DIR, "q2_releases_by_year.csv")
    if not os.path.exists(csv_path):
        return
    df = pd.read_csv(csv_path)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df['release_year'], df['count'], color=NETFLIX_RED, linewidth=3, marker='o', markersize=6)
    ax.fill_between(df['release_year'], df['count'], color=NETFLIX_RED, alpha=0.15)

    ax.set_title("Content Volume by Production Release Year (2000 - 2020)", fontsize=14, weight='bold', pad=15)
    ax.set_xlabel("Release Year", fontsize=11, weight='bold')
    ax.set_ylabel("Number of Titles Released", fontsize=11, weight='bold')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
    ax.grid(True, linestyle='--', alpha=0.6)

    # Highlight peak
    peak_row = df.loc[df['count'].idxmax()]
    ax.annotate(f"Peak: {int(peak_row['release_year'])} ({int(peak_row['count'])} titles)",
                xy=(peak_row['release_year'], peak_row['count']),
                xytext=(peak_row['release_year'] - 4, peak_row['count'] + 50),
                arrowprops=dict(arrowstyle="->", color=NETFLIX_BLACK, lw=1.5),
                fontsize=11, weight='bold', color=NETFLIX_BLACK)

    plt.tight_layout()
    output_path = os.path.join(CHARTS_DIR, "02_releases_by_year.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[+] Generated: {output_path}")

def plot_top_countries():
    """Chart 3: Top 10 Producing Countries (Horizontal Bar Chart)"""
    csv_path = os.path.join(DATA_DIR, "q3_top_10_countries.csv")
    if not os.path.exists(csv_path):
        return
    df = pd.read_csv(csv_path).sort_values(by='count', ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(df['country'], df['count'], color='#B81D24', edgecolor='black', alpha=0.85)

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 25, bar.get_y() + bar.get_height()/2, f"{int(width):,}",
                ha='left', va='center', fontsize=10, weight='bold', color=NETFLIX_BLACK)

    ax.set_title("Top 10 Content Producing Countries on Netflix", fontsize=14, weight='bold', pad=15)
    ax.set_xlabel("Total Titles", fontsize=11, weight='bold')
    ax.grid(axis='x', linestyle='--', alpha=0.6)

    plt.tight_layout()
    output_path = os.path.join(CHARTS_DIR, "03_top_10_countries.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[+] Generated: {output_path}")

def plot_top_ratings():
    """Chart 4: Content Ratings Distribution (Bar Chart)"""
    csv_path = os.path.join(DATA_DIR, "q4_top_ratings.csv")
    if not os.path.exists(csv_path):
        return
    df = pd.read_csv(csv_path)

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(df['rating'], df['count'], color=NETFLIX_RED, edgecolor='black', alpha=0.85)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 30, f"{int(height):,}",
                ha='center', va='bottom', fontsize=9, weight='bold')

    ax.set_title("Content Distribution by Maturity Rating", fontsize=14, weight='bold', pad=15)
    ax.set_xlabel("Maturity Rating", fontsize=11, weight='bold')
    ax.set_ylabel("Total Titles", fontsize=11, weight='bold')
    ax.grid(axis='y', linestyle='--', alpha=0.6)

    plt.tight_layout()
    output_path = os.path.join(CHARTS_DIR, "04_ratings_distribution.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[+] Generated: {output_path}")

def plot_top_genres():
    """Chart 5: Top 10 Genres (Horizontal Bar Chart)"""
    csv_path = os.path.join(DATA_DIR, "q5_top_genres.csv")
    if not os.path.exists(csv_path):
        return
    df = pd.read_csv(csv_path).sort_values(by='count', ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(df['genre'], df['count'], color='#4B6B94', edgecolor='black', alpha=0.9)

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 25, bar.get_y() + bar.get_height()/2, f"{int(width):,}",
                ha='left', va='center', fontsize=10, weight='bold')

    ax.set_title("Top 10 Most Common Genres / Categories on Netflix", fontsize=14, weight='bold', pad=15)
    ax.set_xlabel("Frequency in Catalog", fontsize=11, weight='bold')
    ax.grid(axis='x', linestyle='--', alpha=0.6)

    plt.tight_layout()
    output_path = os.path.join(CHARTS_DIR, "05_top_10_genres.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[+] Generated: {output_path}")

def plot_added_by_year():
    """Chart 6: Platform Ingestion Growth (Titles Added by Year)"""
    csv_path = os.path.join(DATA_DIR, "q6_added_by_year.csv")
    if not os.path.exists(csv_path):
        return
    df = pd.read_csv(csv_path)

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(df['added_year'].astype(str), df['count'], color=NETFLIX_BLACK, edgecolor=NETFLIX_RED, linewidth=1.5)

    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2, height + 30, f"{int(height)}",
                    ha='center', va='bottom', fontsize=9, weight='bold')

    ax.set_title("Platform Catalog Growth: Titles Added to Netflix Annually", fontsize=14, weight='bold', pad=15)
    ax.set_xlabel("Year Ingested onto Platform", fontsize=11, weight='bold')
    ax.set_ylabel("Titles Added", fontsize=11, weight='bold')
    ax.grid(axis='y', linestyle='--', alpha=0.6)

    plt.tight_layout()
    output_path = os.path.join(CHARTS_DIR, "06_titles_added_by_year.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[+] Generated: {output_path}")

def generate_unified_dashboard():
    """Chart 7: Unified 6-Panel Academic Dashboard"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    fig.suptitle("Netflix Big Data Analytics Dashboard (Hadoop HDFS & Apache Hive)", fontsize=18, weight='bold', y=0.98)

    # Panel 1: Content Type
    df1 = pd.read_csv(os.path.join(DATA_DIR, "q1_content_type_distribution.csv"))
    axes[0, 0].pie(df1['count'], labels=df1['type'], autopct='%1.1f%%', colors=[NETFLIX_RED, '#333333'],
                   textprops={'fontsize': 10, 'weight': 'bold'}, wedgeprops=dict(width=0.45, edgecolor='white'))
    axes[0, 0].set_title("1. Movies vs TV Shows", fontsize=12, weight='bold')

    # Panel 2: Releases by Year
    df2 = pd.read_csv(os.path.join(DATA_DIR, "q2_releases_by_year.csv"))
    axes[0, 1].plot(df2['release_year'], df2['count'], color=NETFLIX_RED, linewidth=2, marker='o', markersize=4)
    axes[0, 1].fill_between(df2['release_year'], df2['count'], color=NETFLIX_RED, alpha=0.15)
    axes[0, 1].set_title("2. Titles by Release Year (2000-2020)", fontsize=12, weight='bold')
    axes[0, 1].grid(True, linestyle='--', alpha=0.5)

    # Panel 3: Top Countries
    df3 = pd.read_csv(os.path.join(DATA_DIR, "q3_top_10_countries.csv")).sort_values(by='count', ascending=True)
    axes[0, 2].barh(df3['country'], df3['count'], color='#B81D24', alpha=0.85)
    axes[0, 2].set_title("3. Top 10 Production Countries", fontsize=12, weight='bold')
    axes[0, 2].grid(axis='x', linestyle='--', alpha=0.5)

    # Panel 4: Ratings
    df4 = pd.read_csv(os.path.join(DATA_DIR, "q4_top_ratings.csv"))
    axes[1, 0].bar(df4['rating'], df4['count'], color=NETFLIX_RED, alpha=0.85)
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].set_title("4. Content Maturity Ratings", fontsize=12, weight='bold')
    axes[1, 0].grid(axis='y', linestyle='--', alpha=0.5)

    # Panel 5: Top Genres
    df5 = pd.read_csv(os.path.join(DATA_DIR, "q5_top_genres.csv")).sort_values(by='count', ascending=True)
    axes[1, 1].barh(df5['genre'], df5['count'], color='#4B6B94', alpha=0.85)
    axes[1, 1].set_title("5. Top 10 Genres / Categories", fontsize=12, weight='bold')
    axes[1, 1].grid(axis='x', linestyle='--', alpha=0.5)

    # Panel 6: Added by Year
    df6 = pd.read_csv(os.path.join(DATA_DIR, "q6_added_by_year.csv"))
    axes[1, 2].bar(df6['added_year'].astype(str), df6['count'], color=NETFLIX_BLACK, edgecolor=NETFLIX_RED)
    axes[1, 2].tick_params(axis='x', rotation=45)
    axes[1, 2].set_title("6. Titles Ingested Annually (2008-2020)", fontsize=12, weight='bold')
    axes[1, 2].grid(axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    output_path = os.path.join(CHARTS_DIR, "netflix_analysis_dashboard.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[+] Generated: {output_path}")

def main():
    print("===================================================================")
    print("      Netflix Big Data Project: Visualization Generator            ")
    print("===================================================================")
    plot_content_type()
    plot_releases_by_year()
    plot_top_countries()
    plot_top_ratings()
    plot_top_genres()
    plot_added_by_year()
    generate_unified_dashboard()
    print("===================================================================")
    print(f"[+] All charts successfully generated in: {CHARTS_DIR}")

if __name__ == "__main__":
    main()
