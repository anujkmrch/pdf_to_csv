#!/usr/bin/env python3
import random
import string
import re
import csv
import sys
import os
from nltk import word_tokenize, pos_tag

import pdftotext


class DocumentProcessor(object):
    ''' 
        Searchable pdf, template specific document processing module
     '''
    pdf_text = ''
    pdf_file_path = None
    pdf_to_text = []
    rows = []
    float_regex = None
    db_entity = []

    def __init__(self, pdf_file):
        ''' Initialize the document '''
        self.pdf_file_path = pdf_file
        self.float_regex = re.compile('[+-]?[0-9]+\.[0-9]+')

    def convert_pdf_to_text(self):
        ''' Convert PDF into plain text and split into  lines '''
        with open(self.pdf_file_path, 'rb') as f:
            # return the pdftotext object
            pdf_text = pdftotext.PDF(f)

            # iterate the number of page object,
            # right now we assume there is only one page
            for page in pdf_text:
                self.pdf_text += page
                lines = page.split('\n')
                self.pdf_to_text = lines

    def process_text(self):
        lines = self.pdf_to_text[3:]

        for line in lines:
            string = re.sub('  +', '\t', line)
            columns = string.strip('\n').strip('\r\n')

            cols = []
            col = []
            parts = columns.split('\t')

            for column in parts:

                # Introduced natural language processing technique
                # to separate number and words from sentence
                # could not split with split method

                token = word_tokenize(column)
                # perform entity detection using nltk
                tags = pos_tag(token)

                '''
                    Fixing columns values
                '''
                if len(tags):
                    cd_at_start = False
                    entry = []
                    cd_value = None

                    for index, tag in enumerate(tags):
                        tag_value, tag_type = tag
                        if tag_type == 'CD' and self.float_regex.match(tag_value):
                            if index == 0:
                                cd_at_start = True
                            cd_value = tag_value
                        else:
                            entry.append(tag_value)

                    if cd_at_start:
                        col.append(cd_value)
                        if len(entry):
                            col.append(
                                re.sub(r'\s([?.!"](?:\s|$))', r'\1', " ".join(entry)))

                    elif len(entry):
                        col.append(
                            re.sub(r'\s([?.!"](?:\s|$))', r'\1', " ".join(entry)))
                        if cd_value:
                            col.append(cd_value)

            self.rows.append(col)

        if len(self.rows) > 2:
            self.rows.insert(len(self.rows)-2, [])

    def save_to_csv_and_db_columns(self, csv_file_path):
        """ Method to manage data according to csv and database format """
        with open(csv_file_path, 'w') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)
            for index, row in enumerate(self.rows):
                if row:
                    # ---Start --- Data manipulation for storing eav model entries
                    if index == 0:
                        headers = row[0:3]
                        self.db_entity.append(headers)

                    if index > 0 and not row[0].startswith("Total") and not self.float_regex.match(row[0]):
                        # Maintain Database Enteries First
                        if len(row) > 3:
                            to_entry = row[0:3]
                            by_entry = row[3:]
                            self.db_entity.append(to_entry)
                            self.db_entity.append(by_entry)
                        else:
                            to_entry = row[0:3]
                            self.db_entity.append(to_entry)
                    # ---End--- Data manipulation for storing eav model entries

                    # ---Start--- Manipulate row data to prepare csv file
                    if self.float_regex.match(row[0]):
                        row.insert(0, '')

                    if len(row) > 3 and row[3].startswith("Total"):
                        row.insert(3, '')
                    else:
                        row.insert(4, '')

                    # ---End--- Manipulate row data to prepare csv file
                # Write csv row
                csvwriter.writerow(row)


def process_document(pdf_file_path, csv_file_path):
    """ Document processing function to convert pdf into the csv and save it into database """
    dp = DocumentProcessor(
        pdf_file_path)  # Initialize DocumentProcessor Object with pdf source path

    dp.convert_pdf_to_text()  # Extract pdf text
    dp.process_text()  # Text pre processing and cleaning

    dp.save_to_csv_and_db_columns(csv_file_path)

    head, start_year, end_year = dp.db_entity[0]
    rows = dp.db_entity[1:]
    entries = []

    # EAV entries
    for entry, value_sy, value_ey in rows:
        key_start_year = entry.replace(' ', '-')+'-'+start_year
        key_start_year = key_start_year.lower()
        key_end_year = entry.replace(' ', '-')+'-'+end_year
        key_end_year = key_end_year.lower()

        entries.append({'npa_key': key_start_year, 'npa_val': value_sy})
        entries.append({'npa_key': key_end_year, 'npa_val': value_ey})

    return entries
