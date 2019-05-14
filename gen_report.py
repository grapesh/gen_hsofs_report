#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on 5/14/2019

@author: Sergey.Vinogradov@noaa.gov
"""
import os,sys
import argparse
import glob
import csdlpy
import datetime
import re

#==============================================================================
def timestamp():
    print '------'
    print '[Time]: ' + str(datetime.datetime.utcnow()) + ' UTC'
    print '------'

#==============================================================================
def read_cmd_argv (argv):

    parser = argparse.ArgumentParser()

    parser.add_argument('-i','--hsofsDir',       required=True)
    parser.add_argument('-s','--stormID',        required=True)
    parser.add_argument('-z','--stormCycle',     required=True)
    parser.add_argument('-x','--postfix',        required=True)
    parser.add_argument('-t','--template',       required=True)
    parser.add_argument('-u','--ftpLogin',       required=True)
    parser.add_argument('-f','--ftpPath',        required=True)

    args = parser.parse_args()
    print '[info]: hsofs_post.py is configured with :', args
    return args


#==============================================================================
def run_post(argv):
    #Receive command line arguments
    args = read_cmd_argv(argv)

    #Locate hsofs path
    hsofsPath = args.hsofsDir +'hsofs.'+ args.stormCycle[:-2] + args.postfix + '/'
    if not os.path.exists(hsofsPath):
        print '[error]: hsofs path ' +hsofsPath+ ' does not exist. Exiting'
        return

    ens   = [] #Compile the list of available ensemble members

    fls   = glob.glob(hsofsPath + 'hsofs.' + args.stormID + '.' + \
                    args.stormCycle + '*.surfaceforcing')

    advisoryTrackFile = None
    for f in fls:
        s = os.path.basename(f).split('.')
        print '[debug]: ', s
        ens.append(s[3] +'.'+ s[4] +'.'+ s[5] +'.'+ s[6])
        if s[5] == 'ofcl':
            advisoryTrackFile = f
    print '[info]: ', str(len(ens)),' hsofs ensembles detected: ', ens

    rep = {"_ALIDYYYY_": args.stormID, "_YYYYMMDDHH_" : args.stormCycle}
    rep = dict((re.escape(k), v) for k, v in rep.iteritems())
    pattern = re.compile("|".join(rep.keys()))

    #Read HTM template
    fod = open("index.htm","w")
    with open(args.template,"r") as fid:
        for line in fid:

            if '_ENSEMBLES_LIST_' in line:
                for e in ens:
                    fod.write(e+'<br>\n')

            elif '_MAP_ROW_' in line:
                fod.write('<tr>\n')
                for e in ens:

                    header = '<td rowspan="1" colspan="2" valign="top" bgcolor="#33ff33"><b>' + e + '</b><br>\n</td>\n</tr>'
                    fod.write(header)
                    f_maxele  = './' + args.stormID + '.' + args.stormCycle + '.' + e + '.maxele.png'
                    f_maxwvel = './' + args.stormID + '.' + args.stormCycle + '.' + e + '.maxwvel.png'


                    row = '<td><a href="' + f_maxele + '"><img src="' + f_maxele + '" width="600" border="0"></a><br>\n</td>\n<td><a href="' + f_maxwvel + '"><img src="' + f_maxwvel + '" width="600" border="0"></a><br>\n</td>\n'
                    fod.write(row)
                    fod.write('</tr>\n')

            else:
                fod.write(pattern.sub(lambda m: rep[re.escape(m.group(0))],line))
    fod.close()

    #Upload index
    csdlpy.transfer.upload("index.htm",args.ftpLogin, args.ftpPath)


#==============================================================================
if __name__ == "__main__":

    timestamp()
    run_post (sys.argv[1:])
    timestamp()

