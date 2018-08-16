#!/usr/bin/env python

import optparse
import re
import os


# Use bash dryad-utils/aws-tools/psql_query.sh 'select eperson_id, email, firstname, lastname from eperson'
# to get a file of all epersons

global HOST, DB, USER, PASSWORD
HOST, DB, USER, PASSWORD = None, None, None, None

def sql_query(sql):
    global HOST, DB, USER, PASSWORD
    hostflag, dbflag, userflag, passflag = "", "", "", ""
    if HOST is not None:
        hostflag = ' -h ' + HOST
    if DB is not None:
        dbflag = ' -D ' + DB
    if USER is not None:
        userflag = ' -u ' + USER
    if PASSWORD is not None:
        passflag = ' -p ' + PASSWORD
    
    print "mysql%s%s%s%s -e \"%s\"" % (hostflag, dbflag, userflag, passflag, sql)
    return os.popen("mysql%s%s%s%s -e \"%s\"" % (hostflag, dbflag, userflag, passflag, sql))



def main():
    global HOST, DB, USER, PASSWORD

    parser = optparse.OptionParser()
    parser.add_option("--epersons", dest="eperson_file", help="tab-delimited eperson file")
    parser.add_option("--host", dest="host", help="MySQL server address")
    parser.add_option("--db", dest="database", help="MySQL database")
    parser.add_option("--user", dest="username", help="MySQL username")
    parser.add_option("--password", dest="password", help="MySQL password")
    (options, args) = parser.parse_args()
    print(options)
    if options.host is not None:
        HOST = options.host
    if options.database is not None:
        DB = options.db
    if options.username is not None:
        USER = options.username
    if options.password is not None:
        PASSWORD = options.password
        
    print options.eperson_file
    
    with open(options.eperson_file) as f:
        epersons = f.read().splitlines()
    
    for eperson in epersons:
        print eperson


if __name__ == '__main__':
    main()

