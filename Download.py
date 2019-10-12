import s3fs
import numpy as np
import datetime as dt
import os
import threading


class Thread(threading.Thread):
    def __init__(self, file, path):
#        print('started--->>> ')
        threading.Thread.__init__(self)
        self.file = file
        self.path = path
        
        
    def run(self):
        print('Downloading %s...'%self.file.split('/')[-1])
        start = dt.datetime.now()
        aws = s3fs.S3FileSystem(anon=True)
        aws.get(self.file, '%s/%s'%(self.path, self.file.split('/')[-1]))
        print('Downloaded in %.2f seconds - %s'%(\
                (dt.datetime.now()-start).total_seconds(),
                self.file.split('/')[-1]))
        
        
def to_julian_day(year, month, day):    
    date = dt.datetime.strptime('%d-%d-%d'%(year,month, day), '%Y-%m-%d')    
    return str(date.timetuple().tm_yday).zfill(3)


def download_o(**kargs):
    if kargs.get('day'):
        day = kargs.get('day')
    if kargs.get('month'):
        month = kargs.get('month')
    if kargs.get('year'):
        year = kargs.get('year')
    if kargs.get('ch'):
        ch = kargs.get('ch')
    
    aws = s3fs.S3FileSystem(anon=True)    
    julian_day = to_julian_day(year, month, day)
    bucket = 'noaa-goes16/ABI-L2-CMIPF' 
    query = aws.ls('%s/%d/%s'%(bucket, year, julian_day))
    hours = np.array(query)
    path = 'data/%d/%d/%d'%(year, month, day)
    path = "data_goesr/%s/%s/%s/ch_%s"%(year, month, day, ch)
    
    if not os.path.exists(path):
        os.makedirs(path)


    for hour in hours:
        files = aws.ls(hour)
        for file in files:
            if file.find('M3C'+str(ch)) >= 1:
                thread = Thread(file, path)
                thread.start()
                
                
                
def download(**kargs):
    import datetime as dt
    if kargs.get('day'):
        day = kargs.get('day')
    if kargs.get('month'):
        month = kargs.get('month')
    if kargs.get('year'):
        year = kargs.get('year')
    if kargs.get('ch'):
        ch = kargs.get('ch')
        
    
    aws = s3fs.S3FileSystem(anon=True)    
    julian_day = to_julian_day(year, month, day)
    bucket = 'noaa-goes16/ABI-L2-CMIPF' 
    query = aws.ls('%s/%d/%s'%(bucket, year, julian_day))
    hours = np.array(query)
    path = 'data/%d/%d/%d'%(year, month, day)
    
    if not os.path.exists(path):
        os.makedirs(path)


    for hour in hours:
        files = aws.ls(hour)
        for file in files:
            print(file)
            if file.find('M3C'+str(ch)) >= 1:
                print('Downloading %s...'%file.split('/')[-1])
                
                time = dt.datetime.now()
                year_, month_, day_ = str(time.year), str(time.month).zfill(2), str(time.day).zfill(2)
                hour_, minute_, second_ = str(time.hour).zfill(2), str(time.minute).zfill(2), str(time.second).zfill(2)
            
                time = '%s-%s-%s %s:%s:%s'%(day_, month_, year_, hour_, minute_, second_)
                with open('/home/adriano/Dropbox/log_download_goes.txt', 'a') as f:
                    f.write('%s : STARTED DOWNOLAD, CH %s\n'%(time, ch))
                
                aws.get(file, '%s/%s'%(path, file.split('/')[-1]))
                
                time0 = time
                time = dt.datetime.now()
                year_, month_, day_ = str(time.year), str(time.month).zfill(2), str(time.day).zfill(2)
                hour_, minute_, second_ = str(time.hour).zfill(2), str(time.minute).zfill(2), str(time.second).zfill(2)
            
                time = '%s-%s-%s %s:%s:%s¨'%(day_, month_, year_, hour_, minute_, second_)
                with open('/home/adriano/Dropbox/log_download_goes.txt', 'a') as f:
                    f.write('%s : FINISHED\n'%(time))
                    


if __name__ == "__main__":
    DAY=1
    MONTH=1
    YEAR=2019
    CH=11
    aws = s3fs.S3FileSystem(anon=True)    

    downloadABI(day=DAY, month=MONTH, year=YEAR, ch=CH)