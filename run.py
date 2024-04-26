from wrangling import videos, channels
from utils import *
from countryinfo import CountryInfo


pd.set_option('display.max_columns', None)  # No limit to the number of columns shown
pd.set_option('display.max_rows', None)     # Optional: Display more rows
pd.set_option('display.expand_frame_repr', False)  # Prevent dataframe wrapping


def plot_video_views_scatterplot():
    plt.figure(figsize=(4, 2.5), dpi=300)
    sns.scatterplot(data=channels, x='loggedVideos', y='loggedViews', alpha=0.6, color='grey', edgecolor='none', s=100)
    sns.regplot(data=channels, x='loggedVideos', y='loggedViews', scatter=False, line_kws={'color': 'deepskyblue'})
    sns.regplot(data=channels, x='loggedVideos', y='loggedViews', lowess=True, scatter=False,
                line_kws={'color': 'blue', 'linestyle': '--'})
    sns.set_style("whitegrid")
    plt.xlabel('Log of Videos', fontsize=10, fontweight='bold')
    plt.ylabel('Log of Views', fontsize=10, fontweight='bold')
    plt.title('Channel Videos vs. Views Scatter Plot (Log Scale)', fontsize=10, fontweight='bold')
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.show()


def plot_category_avg_views_barplot():
    category_avg_views = videos.groupby('categoryId')['views'].mean().reset_index()
    category_avg_views = category_avg_views.sort_values('views', ascending=False)
    category_avg_views["categoryId"] = category_avg_views["categoryId"].map(number_to_category)

    plt.figure(figsize=(10, 6))
    sns.barplot(x='views', y='categoryId', data=category_avg_views, palette='Blues_d')

    plt.xlabel('Average Views', fontsize=12)
    plt.ylabel('Category', fontsize=12)
    plt.title('Average Views by Video Category', fontsize=14)
    plt.xticks(fontsize=12)
    plt.tight_layout()
    plt.show()


def plot_days_of_week_boxplots():
    plt.figure(figsize=(12, 6))
    order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    sns.boxplot(x='publishDay', y='loggedViews', data=videos, order=order, palette='coolwarm')

    plt.title('Distribution of Video Views by Day of Week', fontsize=16, fontweight='bold')
    plt.xlabel('Day of Week', fontsize=14, fontweight='bold')
    plt.ylabel('Log of Video Views', fontsize=14, fontweight='bold')
    plt.xticks(fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12, fontweight='bold')
    # plt.yscale('log')
    plt.grid(True, which="both", ls="--", linewidth=0.5, color='gray', axis='y')
    plt.tight_layout()
    plt.show()
    
    
if __name__ == "__main__":
    print(channels['country'].unique())

