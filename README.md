s3clone
=======

Amazon S3 has rather high latency, so bulk downloads in a single
thread are rather slow. This will *quickly* download all of the files
in an S3 bucket by launching a large number of threads to go to S3 in
parallel. Files will be downloaded in order by size (from smallest to
biggest), so download speed by # of files will slow down, while by MB
will speed up. .

Usage: 

    s3clone [bucketname]

Optionally, you can specify a number of worker threads. By default,
this is 100. Optionally, you can specify a prefix, if you would just
like to grab a subdirectory from a bucket. Just be aware S3 is a
little finicky about trailing slashes.

I've used this many times, and this code works for me. It is not well
tested, and so it might not work for you. If you run into issues, give
me a pull request. The biggest bucket I've tested on was 1
terabyte/15,000 files.

It is designed to handle large numbers of small files. For small
numbers of large files, there may be better tools. I don't do parallel
multigets within a single file.

Things to be aware of: 

 * When things fail, error messages are not always all that useful. 
 * If a single file fails, it will tell you, but it won't retry. 
 * Your AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY must be set correctly.
 * I want to be able to use it to update filesystems, so it will
   silently pass over files which already exist. If there is a size
   mismatch, it will tell you. I don't do anything more fancy like
   comparing hashes. For my application, hashing many files would be
   speed-prohibitive. If you don't like this behavior, either feel
   free to do a PR which adds a flag, or just download to an empty
   directory.
 

Requirements: 

 * Python 2.7
 * boto

If a download is interrupted, s3clone will mostly resume, but the
files which were halfway done will stick around in their half-finished
state (I don't like overwriting things by default). If you would like
to flush them, this magic incantation should do it (modulo typos?):

    # Run s3clone to detect mismatched size files
    python s3clone.py edx-all-tracking-logs|tee mismatch
    # Grab the filenames
    cat mismatch |grep Size | cut -d: -f1 > mm
    # Verify the filenames
    less mm
    # Remove them
    cat mm |xargs rm

Enjoy!