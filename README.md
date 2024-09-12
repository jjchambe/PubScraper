# PubScraper

Program 1:  TheScraper.py

-Searches PubMed for all publications from a given year for the affiliation “University of Massachusetts Amherst”

-For each hit, it finds the DOI in the citation and saves the citation including title, authors, etc.

-For each hit/DOI, it visits the doi.org site to view the manuscript

-It then scrolls the browser though the manuscript and takes screenshots

-It then stitches the screenshots together and does OCR to convert it to plain text

-It then does this for the remaining papers from that year
 


Program 2:  TheSearcher.py

-This takes input from an internal webserver that is “user facing” (currently just a VM on a box in my office).

-It collects submitter name, year to search, and keyword list (this is the critical one and I would offer suggestions for 
end user input).

-It also accepts a csv file that contains, in my case, 2 columns listing every trainee who was a facility user and their advisor for a timeframe of 2 years from start of search criteria).

-Then it makes matches based on the names-csv->authors in citation and also keywords->raw text.

-I then apply a weighting to the scores and it outputs a ranked list based on probability that includes the entire citation and hyperlink to paper.


