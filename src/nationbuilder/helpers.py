from datetime import datetime
import urllib

def convertToDbTime(timestamp):
    """ Convert ISO8061 time to database time format """
    
    # Remove non-ascii characters
    timestamp = "".join([i for i in timestamp if ord(i) < 128])
    dt = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    return dt.strftime('%Y-%m-%d %H:%M:%S')