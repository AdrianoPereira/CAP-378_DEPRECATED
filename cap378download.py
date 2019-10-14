from Download import download
import numpy as np

years = [2017]
months = [10]
days = list(range(4, 10))
channels = list(range(1, 17))

for year in years:
    for month in months:
        for day in days:
            for channel in channels:
                channel = '%s'%str(channel).zfill(2)
                path = "data_goesr/%s/%s/%s/ch_%s"%(year, month, day, channel)
                print("Download data to ", path)
                download(year=year, month=month, day=day, ch=channel)
                
                
