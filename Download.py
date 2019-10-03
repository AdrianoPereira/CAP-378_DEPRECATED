import s3fs
import numpy as np
import datetime as dt
import os


def to_julian_day(year, month, day):    
    date = dt.datetime.strptime('%d-%d-%d'%(year,month, day), '%Y-%m-%d')    
    return str(date.timetuple().tm_yday).zfill(3)


def downloadABI(**kargs):
    if kargs.get('day'):
        day = kargs.get('day')
    if kargs.get('month'):
        month = kargs.get('month')
    if kargs.get('year'):
        year = kargs.get('year')
    if kargs.get('ch'):
        ch = kargs.get('ch')
    
    julian_day = to_julian_day(year, month, day)
    bucket = 'noaa-goes16/ABI-L2-CMIPF' 
    query = aws.ls('%s/%d/%s'%(bucket, year, julian_day))
    
    hours = np.array(query)
    
    if not os.path.exists('dados/'+str(YEAR)+'/'+str(MONTH)+'/'+str(DAY)):
        try:
            os.makedirs('dados/'+str(YEAR)+'/'+str(MONTH)+'/'+str(DAY))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    for hour in hours:
        files = aws.ls(hour)
        for file in files:
            if file.find('M3C'+str(ch)) >= 1:
                print('Downloading %s...'%file.split('/')[-1])
                aws.get(file, 'dados/'+str(YEAR)+'/'+str(MONTH)+'/'+str(DAY)+'/'+file.split('/')[-1])      
#        fs.get(files[0], files[0].split('/')[-1])

#    print(files)


if __name__ == "__main__":
    DAY=1
    MONTH=1
    YEAR=2019
    CH=11
    aws = s3fs.S3FileSystem(anon=True)    

    downloadABI(day=DAY, month=MONTH, year=YEAR, ch=CH)