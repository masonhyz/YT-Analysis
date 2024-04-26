import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import pycountry
from countryinfo import CountryInfo
import numpy as np

# mapping from category id to category
number_to_category = {24: "Entertainment",
                      10: "Music",
                      20: "Gaming",
                      1: "Film & Animation",
                      25: "News & Politics",
                      22: "People & Blogs",
                      27: "Education",
                      23: "Comedy",
                      17: "Sports",
                      26: "Howto & Style",
                      28: "Science & Technology",
                      15: "Pets & Animals",
                      19: "Travel & Events",
                      }


def load_channel_data():
    return pd.read_csv('preprocess/channels.csv', sep='\t', encoding='utf-8', na_values='NA')


def load_video_data():
    return pd.read_csv('preprocess/videos.csv', sep='\t', encoding='utf-8', na_values='NA')


def plot_histogram(column, column_name):
    """
    column is pandas series object (numerical) and column name is the x-axis label
    """
    sns.set(style="whitegrid", context="talk", palette="dark")

    plt.figure(figsize=(10, 6))

    ax = sns.histplot(column, kde=True, bins=50, color='blue', line_kws={'linewidth': 2})

    # Set titles and labels
    ax.set_title(f'Distribution of {column_name}', fontsize=20)
    ax.set_xlabel(column_name, fontsize=16)
    ax.set_ylabel('Frequency', fontsize=16)
    ax.tick_params(labelsize=14)

    sns.despine()

    plt.tight_layout()
    plt.show()


def plot_barplot(column, column_name):
    """
    column is pandas series object (categorical) and column name is the x-axis label
    """
    sns.set_style("whitegrid")

    # Create a larger figure size to better fit larger labels and title
    plt.figure(figsize=(8, 6))

    # Create a count plot
    ax = sns.countplot(column, palette='muted')

    # Set larger font sizes and labels with more description if necessary
    ax.set_xlabel(column_name, fontsize=14, labelpad=12)
    ax.set_ylabel('Frequency', fontsize=14, labelpad=12)
    ax.set_title(f'Frequency of Each Category in {column_name}', fontsize=16, pad=12)

    # Set tick parameters
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    # Despine to remove the top and right borders for a cleaner look
    sns.despine()

    # Optionally, you can adjust the bottom margin to make room for the x-labels if they are cut off
    plt.subplots_adjust(bottom=0.15)

    # Show the plot
    plt.show()


def str_to_dt(s):
    return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


def convert_country_codes(code):
    try:
        return pycountry.countries.get(alpha_2=code).alpha_3
    except:
        return None


def get_country_name(code):
    try:
        return pycountry.countries.get(alpha_2=code).name
    except:
        return None


def get_country_longitude(code):
    try:
        return CountryInfo(get_country_name(code)).latlng()[1]
    except:
        return None


def get_country_latitude(code):
    try:
        return CountryInfo(get_country_name(code)).latlng()[0]
    except:
        return None


def get_country_size(code):
    try:
        return CountryInfo(get_country_name(code)).info().get('area')
    except:
        return None


def adjust_coord(original_coord, country_size, scale_factor=0.1):
    std_dev = np.sqrt(country_size) * scale_factor
    adjustment = np.random.normal(0, std_dev)
    return original_coord + adjustment


def int_to_str(n):
    return '{:.3e}'.format(n)

