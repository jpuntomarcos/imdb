# Script for parsing IMDB csv files and loading data into the database

import sqlite3
import csv
import argparse

# Read csv files and SQLite database file from command line
parser = argparse.ArgumentParser(description='Parses IMDB csv files and loading data into the database')
parser.add_argument("movies_data_file", help="Movies csv file", type=str)
parser.add_argument("ratings_data_file", help="Ratings csv file", type=str)
parser.add_argument("sqlite_file", help="SQLite database file", type=str)
args = parser.parse_args()

# Connect to the SQLite database
conn = sqlite3.connect(args.sqlite_file)
cursor = conn.cursor()

# Read data from the ratings_data_file and store in a dict
ratings = {}
with open(args.ratings_data_file, encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    for row in reader:
        ratings[row['tconst']] = row['averageRating']

# Insert data from the movie_data.tsv file
categories_db = {}  # dict of categories {name, id}
with open(args.movies_data_file, encoding='utf-8') as csvfile:

    # Read csv file
    reader = csv.reader(csvfile, delimiter='\t')
    next(reader)  # skip header row

    # Process each line
    for row in reader:

        # Replace "\N" with None
        row = [None if x == r"\N" else x for x in row]

        # Get fields
        tconst, title, year, runtime, genres = row
        rating = ratings.get(tconst)  # get rating from previous dict

        # Insert into DB
        cursor.execute('''
            INSERT INTO IMDB_movie (title, imdb_tconst, year, runtime, rating)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, tconst, year, runtime, rating))
        movie_id = cursor.lastrowid

        # Parse and insert category data
        row_categories = []
        if genres is not None:
            row_categories = genres.split(',')
        missing_categories = set(row_categories) - categories_db.keys()
        for category_name in missing_categories:
            cursor.execute(''' INSERT INTO IMDB_category (name) VALUES (?) ''', (category_name,))
            categories_db[category_name] = cursor.lastrowid

        for name in row_categories:
            category_id = categories_db[name]
            cursor.execute(''' INSERT INTO IMDB_movie_category (movie_id, category_id) VALUES (?, ?)''',
                           (movie_id, category_id))

# Commit the changes and close the connection
conn.commit()
conn.close()
