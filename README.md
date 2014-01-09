s3clone
=======

Amazon S3 has rather high latency, so bulk downloads in a single
thread are rather slow. This will *quickly* download all of the files
in an S3 bucket by launching a large number of threads to go to S3 in
parallel.

Usage: 

    s3clone [bucketname]

Optionally, you can specify a number of worker threads. By default,
this is 100.

This code works for me. It is not well tested, and no guarantees it
will work for you. In particular: 

 * When things fail, error messages are not at all useful. 
 * Your AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY must be set correctly.