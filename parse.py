# -*- coding: utf-8 -*-
# Some functions that will help with parsing lexisnexis results
import sys
import getopt
import re
import glob
import argparse
import csv
import os.path

def getcolumns(fullstr,percent=10):
    """
    Return the names of the columns for which we have metadata.

    Keyword arguments:
    fullstr -- The full text of the lexisnexis file, in a string.
    percent -- The minimum percentage of occurences needed to include a column.
               (default: 10)
    """
    cols = re.findall("\n([A-Z\-]+): .+",fullstr)
    d = dict()
    for c in cols:
        if c in d:
            d[c] += 1
        else:
            d[c] = 1

    return [c for c in d.keys() if d[c]>(max(d.values())*percent/100.0)]

def splitdocs(fullstr,topmarker="LENGTH",bottommarker="LOAD-DATE",colnames=["LENGTH"]):
    """
    Return a list of dictionaries containing articles and metadata.

    In general, this script will attempt to pull the text between the topmarker and bottommarker.
    If the topmarker and bottommarker are not found, the text will not be included.
    Keyword arguments:
    fullstr -- The full text of the lexisnexis results, in a string
    topmarker -- The last piece of metadata before an article (default: "LENGTH")
    bottommarker -- The first piece of metadata after an article (default: "LOAD-DATE")
    colnames -- The list of metadata names in a list (default: ["LENGTH"])
    """

    if colnames is None or len(colnames)==0:
        colnames = ["LENGTH"]
    # process the column names for the copyright line
    if colnames is not None and len(colnames)>0:
        oldcolnames = colnames
        colnames = []
        docopyright = False
        for c in oldcolnames:
            if c.upper() != 'COPYRIGHT':
                colnames.append(c)
            else:
                # copyright is handled differently, but people can enter it the same way
                docopyright = True

    allsplits = re.split("\d+ of \d+ DOCUMENTS.+?",fullstr)
    articles = []
    for i,s in enumerate(allsplits[1:]):
        #import code; code.interact(local=locals())
        if topmarker is not None and re.search("\n"+topmarker+".+?\n",s) is not None:
            headersplit = re.split("\n"+topmarker+".+?\n",s)
            header = headersplit[0]
            body = headersplit[1]
        else:
            header = ''
            body = s
            if topmarker is not None:
                print "*** Marker", topmarker, "not found in article", i+1
        if bottommarker is not None and re.search("\n"+bottommarker+".+?\n",body) is not None:
            bottomsplit = re.split("\n"+bottommarker+".+?\n",body)
            body = bottomsplit[0]
            footer = bottomsplit[1]
        else:
            footer = ''
            body = body
            if bottommarker is not None:
                print "*** Marker", bottommarker, "not found in article", i+1

        d = dict.fromkeys(colnames)
        d['text'] = body.strip()
        for c in colnames:
            res = re.findall("\n"+c+":(.+)?\r",s)
            if len(res)>0:
                d[c] = res[0].strip()
        if docopyright:
            try:
                #import code; code.interact(local=locals())
                copyresult = re.findall(r'\n\s+(Copyright|\N{COPYRIGHT SIGN}|©)\s+(.*)\n',s,flags=re.IGNORECASE)
                d['COPYRIGHT'] = copyresult[0][1].strip()
            except:
                print "*** Copyright line not found in article", i+1
        articles.append(d)
    return articles

def main():
    parser = argparse.ArgumentParser(description='Parse output from Lexis Nexis.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d','--directory', help='the path containing multiple lexis nexis files (e.g. /users/me/data)', required=False, nargs=1)
    group.add_argument('-f','--file', help='individual file(s) to process (e.g. /Users/jdoe/Downloads/foo.txt)', required=False, nargs='*')
    parser.add_argument('-c','--csvfile', help='the csv file containing the metadata', required=False, nargs=1)
    parser.add_argument('-o','--outfiles', help='the directory to write individual articles to', required=False, nargs=1)
    parser.add_argument('-m','--metadata', help='the metadata to scrape from individual articles', required=False, nargs='*')
    parser.add_argument('-b','--boundaries', help='the metadata before an article begins, and after it ends.  If there is only a beginning or ending metadata tag, use None.', required=False, nargs=2)

    args = vars(parser.parse_args())

    if args['directory'] is not None:
        files = glob.glob(args['directory'][0]+os.path.sep+'*.txt') + glob.glob(args['directory'][0]+os.path.sep+'*.TXT')
    elif args['file'] is not None:
        files = args['file']

    fieldnames = []
    if args['outfiles'] is not None:
        fieldnames += ['filename','originalfile']
    if args['metadata'] is not None:
        fieldnames += args['metadata']
    if args["csvfile"] is not None:
        fcsv = open(args["csvfile"][0],'w')
        dw = csv.DictWriter(fcsv, delimiter='\t', fieldnames=fieldnames)
        dw.writeheader()
    else:
        fcsv = False

    if args["boundaries"] is not None:
        bstart = args["boundaries"][0]
        if bstart == 'None':
            bstart = None
        bend = args["boundaries"][1]
        if bend == 'None':
            bend = None

    if args["boundaries"] is not None:
        bstart = args["boundaries"][0]
        if bstart == 'None':
            bstart = None
        bend = args["boundaries"][1]
        if bend == 'None':
            bend = None

    outputs = []

    counter = 0
    for f in files:
        fp = open(f,'r')
        print "Processing file: ", f
        #splitdocs(fullstr,topmarker="LENGTH",bottommarker="LOAD-DATE",colnames=["LENGTH"]):
        if args['boundaries'] is not None:
            outputs = splitdocs(fp.read(),topmarker=bstart,bottommarker=bend,colnames=args['metadata'])
        else:
            outputs = splitdocs(fp.read(),colnames=args['metadata'])
        print "...............{} articles found".format(len(outputs))
        if args["outfiles"] is not None:
            for art in outputs:
                #import code; code.interact(local=locals())
                fname = "{direc}{sep}{c:08d}.txt".format(direc=args['outfiles'][0],,sep=os.path.sep,c=counter)
                fw = open(fname,'w')
                fw.write(art['text'])
                counter+=1
                fw.close()
                if fcsv:
                    art.pop('text')
                    art['filename'] = fname
                    art['originalfile'] = f
                    dw.writerow(art)
        elif fcsv:
            for art in outputs:
                art.pop('text')
                dw.writerow(art)

    if fcsv:
        fcsv.close()


if __name__ == '__main__':
    main()
