s3clone
=======

Amazon S3 has rather high latency, so bulk downloads in a single
thread are rather slow. This will *quickly* download all of the files
in an S3 bucket by launching a large number of threads to go to S3 in
parallel. Files will be downloaded in order by size. 

Usage: 

    s3clone [bucketname]

Optionally, you can specify a number of worker threads. By default,
this is 100.

This code works for me. It is not well tested, and it probably won't work for you. 

Things to be aware of: 

 * When things fail, error messages are not at all useful. 
 * Your AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY must be set correctly.
 * It will silently pass over files which exist. It ought to compare
   sizes, hashes, or similar. It doesn't. 

Requirements: 

 * Python 2.7
 * boto