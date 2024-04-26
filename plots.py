from utils import *
import plotly.express as px
from wrangling import videos, channels
import random
import ast


## Fig 1
fig11 = px.scatter_3d(channels, x='subscribers', y='videos', z='views',
                     title='Channel Total Views Scatterplot Against Channel Videos and Subscribers',
                     labels={'subscribers': 'Subscribers', 'videos': 'Videos', 'views': 'Total Views'},
                     log_x=True, log_y=True, log_z=True,
                     color='loggedViews',  # Color by subscribers for additional visual information
                     color_continuous_scale=px.colors.sequential.Viridis)  # Using a sequential color scale

fig11.update_layout(
    margin=dict(l=0, r=0, b=0, t=150),  # Reducing the plot margins
    scene=dict(
        xaxis_title='Subscribers (log scale)',
        yaxis_title='Videos (log scale)',
        zaxis_title='Total Views (log scale)',
        xaxis=dict(tickfont=dict(size=15), title_font=dict(size=20)),
        yaxis=dict(tickfont=dict(size=15), title_font=dict(size=20)),
        zaxis=dict(tickfont=dict(size=15), title_font=dict(size=20)),
    ),
    font=dict(
        family="Arial, sans-serif",
        size=20,
        color="DarkSlateGrey"
    )
)


fig12 = px.scatter_3d(videos, x='comments', y='likes', z='views',
                     title='Video Views Scatterplot Against Video Comments and Likes',
                     labels={'comments': 'Comments', 'likes': 'Likes', 'views': 'Video Views'},
                     log_x=True, log_y=True, log_z=True,
                     color='loggedViews',  # Color by likes for additional visual information
                     color_continuous_scale=px.colors.sequential.Cividis)  # Using a different sequential color scale

fig12.update_layout(
    margin=dict(l=0, r=0, b=0, t=150),
    scene=dict(
        xaxis_title='Comments (log scale)',
        yaxis_title='Likes (log scale)',
        zaxis_title='Video Views (log scale)',
        xaxis=dict(tickfont=dict(size=15), title_font=dict(size=20)),
        yaxis=dict(tickfont=dict(size=15), title_font=dict(size=20)),
        zaxis=dict(tickfont=dict(size=15), title_font=dict(size=20)),
    ),
    font=dict(
        family="Arial, sans-serif",
        size=20,
        color="DarkSlateGrey"
    )
)


## Fig 2
fig2 = px.histogram(videos[videos['durationCategory'].notna()], x="loggedViews",
                    color="caption",  # Differentiates histograms by caption status
                    barmode='overlay',  # Overlays the histograms on top of each other
                    facet_col="durationCategory",  # Facets by duration category
                    title="Histogram of Views (log scale) by Duration Category and Caption Status",
                    category_orders={"durationCategory": ["Short", "Medium", "Long"]},
                    labels={"loggedViews": "Views (log scale)"},
                    color_discrete_map={True: 'blue', False: 'red'},  # Color mapping for clarity
                    height=600, width=800,
                    nbins=20)

fig2.update_layout(
    margin=dict(l=0, r=0, b=0, t=150),
    title_font_size=20,
    font=dict(
        family="Arial, sans-serif",
        size=15,
        color="DarkSlateGrey"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    bargap=0,
)

fig2.update_traces(opacity=0.7)
fig2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))


## Fig 3
categories = ['News & Politics', 'Music', 'Gaming', 'Education', 'Film & Animation', 'Entertainment']
filtered_videos = videos[videos['categoryName'].isin(categories)]
color_map = {
    'News & Politics': 'rgba(25, 25, 112, 0.9)',    # Midnight Blue
    'Education': 'rgba(60, 60, 230, 0.9)',         # BlueViolet
    'Music': 'rgba(220, 20, 60, 0.9)',              # Crimson
    'Gaming': 'rgba(255, 69, 0, 0.9)',              # Red-Orange
    'Film & Animation': 'rgba(255, 140, 0, 0.9)',   # Dark Orange
    'Entertainment': 'rgba(205, 92, 92, 0.9)'       # Indian Red
}

fig3 = px.box(filtered_videos, x='publishDay', y='loggedViews',
             color='categoryName',  # Differentiate by category
             color_discrete_map=color_map,  # Apply custom color map directly here
             title="Video Views by Day of Week for Selected Categories",
             labels={"loggedViews": "Video Views (log scale)", "publishDay": "Day of Week", "categoryName": "Category"},
             category_orders={"publishDay": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                              "categoryName": ['News & Politics', 'Education', 'Entertainment', 'Film & Animation', 'Music', 'Gaming']},  # Maintain a logical order
             height=600, width=1000)

# Update layout to display boxplots side by side within each day
fig3.update_layout(
    title_font_size=20,
    font=dict(family="Arial, sans-serif", size=12, color="DarkSlateGrey"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    boxmode='group'  # Group boxplots by x-axis category
)


## Fig 4
geo_channels = channels[['views', 'loggedViews', 'country', 'username', 'topicsSuper']].copy()
geo_channels['topicsSuper'] = geo_channels['topicsSuper'].apply(ast.literal_eval).apply(random.choice)
geo_channels['longitude'] = geo_channels['country'].apply(get_country_longitude)
geo_channels['latitude'] = geo_channels['country'].apply(get_country_latitude)
geo_channels['countryNew'] = geo_channels['country'].apply(convert_country_codes)
geo_channels['size'] = geo_channels['country'].apply(get_country_size)
geo_channels['new_lat'] = geo_channels.apply(
    lambda row: adjust_coord(row['latitude'], row['size'], scale_factor=0.0011), axis=1
)
geo_channels['new_long'] = geo_channels.apply(
    lambda row: adjust_coord(row['longitude'], row['size'], scale_factor=0.0011), axis=1
)
country_views = geo_channels.groupby('countryNew')['views'].sum().reset_index()
geo_channels = geo_channels.merge(country_views, on='countryNew', suffixes=('', 'Total'))
# hack to sacrifice some space but make the hover better looking
geo_channels['Country'] = geo_channels['countryNew']
geo_channels['Topic'] = geo_channels['topicsSuper']
geo_channels['Views'] = geo_channels['views'].apply(int_to_str)
geo_channels['Total views of the country'] = geo_channels['viewsTotal'].apply(int_to_str)

fig4 = px.scatter_geo(geo_channels,
                     lat='new_lat',
                     lon='new_long',
                     color="Topic",
                     size="views",
                     hover_name="username",
                     hover_data={"views": False, "Views": True, "Country": True, "new_long": False,
                                 "new_lat": False, "Topic": True, "Total views of the country": True},
                     title="Channel Total Views by Category and Country",
                     # projection="natural earth",
                     )
# fig4 = px.choropleth(country_views,
#                      locations="countryNew",
#                      color="views",
#                      hover_name="countryNew",
#                      color_continuous_scale=px.colors.sequential.Jet,
#                      labels={'views': 'Views'},
#                      title="Video Views by Country")
fig4.update_traces(marker=dict(showscale=False))
fig4.update_geos(
    showcountries=True, countrycolor="RebeccaPurple"
)
fig4.update_layout(
    # geo=dict(
    #     showframe=False,
    #     showcoastlines=False,
    #     projection_type='equirectangular'
    # ),
    geo=dict(
        showland=True,
        # landcolor="lightgrey",
        showcountries=True,
        showcoastlines=True,
        # countrycolor="darkgrey",
        showocean=True,
        oceancolor="azure"
    ),
    annotations=[dict(
        x=0.55,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: Channels Dataset',
        showarrow=False
    )]
)


if __name__ == "__main__":
    fig4.show()
