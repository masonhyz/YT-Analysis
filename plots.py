from utils import *
import plotly.express as px


channels = load_channel_data()
videos = load_video_data()


fig1 = px.scatter_3d(channels, x='subscribers', y='videos', z='views',
                    title='Channel Statistics',
                    labels={'subscribers': 'Subscribers', 'videos': 'Videos', 'views': 'Views'},
                    log_x=True, log_y=True, log_z=True)


