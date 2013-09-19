lexisparse
==========

A simple tool to process plain text output from Lexis Nexis news searches

Example Call
----------------
`python parse.py -d docs/ -b LENGTH None -c tjtest.csv -o docs/ -m LOAD-DATE LENGTH PUBLICATION-TYPE LANGAUGE SECTION`

* You must use python version 2.7 (e.g., calling python2.7 if necessary)
* `-d` is where the script will look for your lexis nexis text files
* `-b` specifies the boundaries above and below the article text (None can be used to include everything above or below)
  Note that documents are bounded by at the very least `[Number] of [Other Number] DOCUMENTS` - this is what will be the boundary if it is left blank or set as `None`.
* `-c` specifies the name of the csv file to write output to
* `-o` specifies the location to write the output text files (one per article)
* `-m` specifies the metadata to look for in a document.  Not every document needs to have this metadata!  It can only find metadata that is followed by a colon at the beginning of a line.