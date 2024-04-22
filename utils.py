import pandas as pd


def load_channel_data():
    return pd.read_csv('preprocess/channels.csv', sep='\t', encoding='utf-8', na_values='NA')


def load_video_data():
    return pd.read_csv('preprocess/videos.csv', sep='\t', encoding='utf-8', na_values='NA')
