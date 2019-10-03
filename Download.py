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
    
    if not os.path.exists(path):
        os.makedirs(path)


    for hour in hours:
        files = aws.ls(hour)
        for file in files:
            if file.find('M3C'+str(ch)) >= 1:
                thread = Thread(file, path)
                thread.start()
                
                
                
def download(**kargs):
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
                aws.get(file, '%s/%s'%(path, file.split('/')[-1]))


if __name__ == "__main__":
    DAY=1
    MONTH=1
    YEAR=2019
    CH=11
    aws = s3fs.S3FileSystem(anon=True)    

    downloadABI(day=DAY, month=MONTH, year=YEAR, ch=CH)