from utils import *
import numpy as np


channels = load_channel_data()
videos = load_video_data()

# log transform for channels numerical variables
channels['loggedViews'] = np.log10(channels['views'] + 1)
channels['loggedVideos'] = np.log10(channels['videos'] + 1)
channels['loggedSubscribers'] = np.log10(channels['subscribers'] + 1)

# remove channels without videos and those without views, and those with less than 10 million subs
channels = channels[channels['loggedSubscribers'] >= 7]
channels = channels[channels['loggedViews'] > 0]
channels = channels[channels['loggedVideos'] > 0]

# log transform for videos numerical variables
videos['loggedViews'] = np.log10(videos['views'] + 1)
videos['loggedLikes'] = np.log10(videos['likes'] + 1)
videos['loggedComments'] = np.log10(videos['comments'] + 1)
videos['loggedSeconds'] = np.log10(videos['durationSeconds'] + 1)

# datetime tranforms
videos['publishedDate'] = videos['publishedDate'].apply(str_to_dt)
videos['publishDay'] = videos['publishedDate'].dt.day_name()
videos['publishHour'] = videos['publishedDate'].dt.hour

# category id to name
videos['categoryName'] = videos['categoryId'].map(number_to_category)

# duration and views categorization
bin_edges = [0, 1.9, 2.7, 1000]  # Adjust these values based on your specific needs
videos['durationCategory'] = pd.cut(videos['loggedSeconds'], bins=bin_edges, labels=["Short", "Medium", "Long"],
                                    include_lowest=True)




if __name__ == "__main__":
    print(videos.info())
    # plot_histogram(channels['loggedVideos'], 'Log of Videos')
    # plot_histogram(channels['loggedViews'], 'Log of Views')
    # plot_histogram(channels['loggedSubscribers'], 'Log of Subscribers')
    #
    plot_histogram(videos['views'], 'Views')
    plot_histogram(videos['likes'], 'Likes')
    plot_histogram(videos['comments'], 'Comments')
    plot_histogram(videos['durationSeconds'], 'Duration')
    #
    # plot_histogram(videos['loggedViews'], 'Log of Video Views')
    # plot_histogram(videos['loggedLikes'], 'Log of Video Likes')
    # plot_histogram(videos['loggedComments'], 'Log of Video Comments')
    # plot_histogram(videos['loggedSeconds'], 'Log of Video Durations')
    #
    # plot_barplot(videos['categoryName'], 'Category')
    # plot_barplot(videos['durationCategory'], 'Duration')
    # plot_barplot(videos['publishDay'], 'Published day of week')


