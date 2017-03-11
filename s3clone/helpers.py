import argparse
import gzip
import shutil
import os
import os.path

parser = argparse.ArgumentParser(description="Download a bucket from S3")
parser.add_argument('--workers', '-n', metavar='N', type=int,
                    help="Number of worker threads", default=100)
parser.add_argument('--prefix', '-p', metavar='prefix', type=str,
                    help="Prefix of files to get", default="")
parser.add_argument('--outputdir', '-o', metavar='outputdir', type=str,
                    help="Output directory", default=".")
parser.add_argument('--gzip', dest='gzip', action='store_true',
                    help="Compress files")
parser.add_argument('--role', type=str,
                    help='AIM role as defined in .aws/config')
parser.add_argument('bucket', metavar='<s3 bucket>', type=str,
                    help="S3 bucket to download")


def list_objects(client, bucket, prefix):
    '''
    List all the objects in an S3 bucket. This function handles
    pagination, which boto2 did for us, but boto3 doesn't seem to.
    '''
    response = client.list_objects_v2(Bucket = bucket, Prefix=prefix)
    while response:
        for item in response['Contents']:
            yield item['Key'], item['Size']
        if response['IsTruncated']:
            try:
                response = client.list_objects_v2(Bucket = bucket, Prefix=prefix, ContinuationToken=response['NextContinuationToken'])
            except KeyError:
                print response
                print response['IsTruncated']
                print response.keys()
                raise
        else:
            response = None


def download(client, bucket, key, filename, gzip_file=False):
    '''
    Download a single file from Amazon S3. Compress if necessary.
    '''
    # This try/except clause avoids threading conflict issues and
    # similar. It is overly broad, but if it fails, errors will still
    # be caught if this fails at the time of the attempted download.
    # This avoids issues such as worker thread contention, where two
    # try to create the same directory, as might happen with simply
    # creating a dir if it does not exist.
    try:
        os.makedirs(os.path.dirname(filename))
    except:
        pass
    client.download_file(bucket, key, filename)
    if gzip_file:
        if not filename.endswith(".gz"):
            with open(filename, 'rb') as f_in, \
                 gzip.open(filename+'.s3clonegz.gz', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            os.unlink(filename)

