import pandas as pd
from server.data.sql_data_service import SqlDataService
from server.model.video import Video
import time

##################################################################
# Modify for next sets
index = 1
##################################################################

file_path = f'videos_set_{index}.csv'
df = pd.read_csv(file_path)

print(df.head(5))

print('\n--started storing videos--')
data_service = SqlDataService()
for index, row in df.iterrows():
    video = Video(
        video_id = row['video_id'], 
        title = row['title'], 
        categories = row['categories'], 
        duration = row['duration'], 
        tags = '' if pd.isna(row['tags']) else row['tags'], 
        publish_date = row['publish_date'],
        vector = row['vector']
    )
    data_service.insert_video(video)

print('--finished storing videos--')