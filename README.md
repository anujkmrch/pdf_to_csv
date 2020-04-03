# PDF TO CSV CONVERSION

Python based template specific searchable pdf to csv table extratction.

# Files

** DocumentProcessing** is the utility module to convert file into text and then map to csv column according to the template specific code. It is using some **natural language processing (NLP) ** technique to map the template according to the

## DB Model

It is having slug specific CSV storage map and every entry belongs to some csv. It can also improve the reduntancy among columns for multiple case.
Primarily it is using EAV model for the database design.

## Requirements

It require only three libraries to run this project, django, nltk, pdftotext

## Disclaimer

It is just and assignment for agrevolution.in, just like a quick and simple **P-O-C**
Please do not use it for live and production ready.
