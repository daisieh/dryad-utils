#!/usr/bin/env python

# List av-status tags for every object in a bucket

__author__ = 'daisie'

import os
import re
import sys
import json
import hashlib

def main():
    if len(sys.argv) < 2:
        print "Bucket is required as argument"
        exit(0)
    bucket = sys.argv[1]
    
    count = 0
    keys = []

    if len(sys.argv) == 4:
        keys_file = sys.argv[3]
        with open(keys_file) as f:
            keys = f.read().splitlines()
    else:
        # collect all the keys from the bucket:
        next_token = " "
        if len(keys) == 0:
            while next_token is not "":
                base_cmd = 'aws s3api list-objects-v2 --bucket %s --page-size 1000 --max-items 1000 %s' % (bucket, next_token)
                results = json.load(os.popen(base_cmd))
                if results is None:
                    print "empty bucket"
                    exit(1)

                if 'NextToken' in results:
                    next_token = '--starting-token ' + results['NextToken']
                else:
                    next_token = ""

                for object in results['Contents']:
                    keys.append(object['Key'])
                for key in keys:
                    count = count + 1
                    if (re.match("^\.", key) is None):
                        cmd = 'aws s3api get-object-tagging --bucket %s --key "%s"' % (bucket, key)
                        metadata = json.load(os.popen(cmd))
                        if 'TagSet' in metadata:
                            for tagpair in metadata['TagSet']:
                                if tagpair['Key'] == 'av-status':
                                    print "(%s) %s: %s" % (count, key, tagpair['Value'])
                    sys.stdout.flush()
                keys = []

    print "added %s keys" % (len(keys))
    sys.stdout.flush()
    
if __name__ == '__main__':
    main()
