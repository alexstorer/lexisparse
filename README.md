lexisparse
==========

A simple tool to process plain text output from Lexis Nexis news searches

Requirements
---
* Python 2.7 or higher

_It is possible to write a backward compatible version if necessary_


Features
------
* Extract individual articles
* Pull metadata from articles, e.g., lines beginning with [WORD]:
* Let users define article start and stop boundaries
* Pull information from Copyright line
* Extract CSV containing metadata
* Read in from single lexisnexis text files, multiple files or a directory

Example Call
----------------
`python parse.py -d docs/ -b LENGTH None -c tjtest.csv -o docs/ -m LOAD-DATE LENGTH PUBLICATION-TYPE LANGAUGE SECTION`

This asks the script to...

Read in documents from the `docs` directory, and write out documents to the `docs` directory.  Write an index file including metadata entitled `tjtest.csv`.  Document bodies begin with "LENGTH:" but do not have a consistent ending string.

Full Options
--------

* `-d` is where the script will look for your Lexis Nexis text files
* `-b` specifies the boundaries above and below the article text (None can be used to include everything above or below)
  Note that documents are bounded by at the very least `[Number] of [Other Number] DOCUMENTS` - this is what will be the boundary if it is left blank or set as `None`.  `-b LENGTH None` specifies that the article body begins after a line that starts with `LENGTH:` and ends at the end of the document.  The boundaries may differ depending on which files you have exported from Lexis Nexis - in the event that a boundary is not found, the article header and footer will be included.
* `-c` specifies the name of the csv file to write output to
* `-o` specifies the location to write the output text files (one per article)
* `-m` specifies the metadata to look for in a document.  Not every document needs to have this metadata!  It can only find metadata that is followed by a colon at the beginning of a line.  _Copyright can also be included as a potential metadata field, and will not be expected to begin a line followed by a colon._
