import argparse
import os
import threading
import time
import Queue

from boto.s3.connection import S3Connection

import humanize

DEBUG = False

parser = argparse.ArgumentParser(description = "Download a bucket from S3")
parser.add_argument('--workers', '-n', metavar='N', type=int, help="Number of worker threads", default = 100)
parser.add_argument('bucket', metavar='<s3 bucket>', type=str, help="S3 bucket to download")

args = parser.parse_args()

print "Workers", args.workers

conn = S3Connection()
bucket = conn.get_bucket(args.bucket)
items = bucket.list()
#items = [(i.name, i.size, i) for i in items]

def download(key):
    #if os.path.dirname(key.name) and not os.path.exists(os.path.dirname(key.name)):
    # Try/except avoids threading conflict issues. Errors will still
    # be caught if this fails at the time of the attempted download.
    # Without this, occasionally two workers will contend, try to
    # create the same directory, and fail
    try:
        os.makedirs(os.path.dirname(key.name))
    except: 
        pass 
    if not os.path.exists(key.name):
        key.get_contents_to_filename(key.name)

task_queue = Queue.PriorityQueue()
lock = threading.Lock()
size = 0

def worker():
    while True:
        item = task_queue.get()
        if DEBUG:
            print "Grabbing", item
        try: 
            download(item)
            with lock:
                global size
                size = size - item.size
        except:
            print "Download of ", item, "failed"
        task_queue.task_done()

print "Queuing bucket..."

count  = 0
for item in items:
    task_queue.put(item, -item.size)
    count = count + 1
    size = size + item.size
    
print "Running workers..."

for i in range(args.workers):
    t = threading.Thread(target = worker)
    t.daemon = True
    t.start()

print "Workers started..."

while not task_queue.empty():
    time.sleep(0.1)
    print "Downloading. ", task_queue.unfinished_tasks, " files remaining, (", count , ")",  humanize.bytes(size),"\r",


task_queue.join()

print "Done"
