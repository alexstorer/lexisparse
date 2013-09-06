# Some functions that will help with parsing lexisnexis results

import re

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

    Keyword arguments:
    fullstr -- The full text of the lexisnexis results, in a string
    topmarker -- The last piece of metadata before an article (default: "LENGTH")
    bottommarker -- The first piece of metadata after an article (default: "LOAD-DATE")
    colnames -- The list of metadata names in a list (default: ["LENGTH"])
    """
    allsplits = re.split("\d+ of \d+ DOCUMENTS.+?",fullstr)
    articles = []
    for s in allsplits[1:]:
        d = dict.fromkeys(colnames)
        headsplit = re.split("\n"+topmarker+".+?\n",s)
        d['text'] = re.split("\n"+bottommarker+".+?\n",headsplit[1])[0].strip()
        for c in colnames:
            res = re.findall("\n"+c+":(.+)?\r",s)
            if len(res)>0:
                d[c] = res[0].strip()
        articles.append(d)
    return articles