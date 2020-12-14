import datetime
from datetime import timedelta
import glob
import os
# from Pinnutil.FTP_Module import ftpExt
import ftplib

defaultInterval = timedelta(minutes=10)

if __name__ == '__main__':
    varianServer = 'Y:\\'

    now = datetime.datetime.now()
    print(now.year, now.month, now.day, now.hour,now.minute)
    
    ftpEnty = ftplib.FTP('10.36.126.63')
    ftpEnty.login('p3rtp','qaandqc9')
    # ftpEnty.retrlines('LIST')
    ftpEnty.cwd('/files/network/DICOM')
    # ftpEnty.retrlines('LIST')
    # ftpEnty.changepath('/files/network/DICOM')
    # ftpEnty.show()
    # for dirpath, dirnames, filenames in os.walk(varianServer):
    #     for dir in dirnames:
    with os.scandir(varianServer) as entities:
        for entry in entities:
            info = entry.stat()
            time_entry = datetime.datetime.fromtimestamp(info.st_mtime)
            # print("%s:%s"%(entry.name,info.st_mtime))
            # print('%s:%s'%(entry.name,time_entry))
            delta_time = now - time_entry
            print('pat:%s;passtiem：%s'%(entry.name,delta_time))
            if (delta_time < defaultInterval):
                transDirPath = os.path.join(varianServer,entry.name)
                with os.scandir(transDirPath) as dicomEntry:
                    for entry in dicomEntry:
                        curfile = open(os.path.join(transDirPath,entry.name),'rb')
                        ftpEnty.storbinary('STOR %s' %entry.name,curfile)
                        curfile.close()
                        print('success:%s' %entry.name)

    ftpEnty.close()
