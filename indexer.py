import lucene
import csv
import unittest

from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, TextField, StringField
from org.apache.lucene.index import IndexOptions, IndexWriter, IndexWriterConfig, DirectoryReader, Term
from org.apache.lucene.store import MMapDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.search import BooleanQuery, BooleanClause, TermQuery, TermRangeQuery


lucene.initVM(vmargs=['-Djava.awt.headless=true'])


def index_csv_data(csv_data, index_writer):
    for row in csv_data:
        doc = Document()
        doc.add(StringField("name", row[0], Field.Store.YES))
        doc.add(StringField("team", row[1], Field.Store.YES))
        doc.add(StringField("round", row[2], Field.Store.YES))
        doc.add(StringField("overall", row[3], Field.Store.YES))
        doc.add(StringField("year", row[4], Field.Store.YES))
        doc.add(StringField("position", row[5], Field.Store.YES))
        doc.add(StringField("nationality", row[6], Field.Store.YES))
        doc.add(StringField("junior_team", row[7], Field.Store.YES))
        index_writer.addDocument(doc)


with open("output_merged.csv", "r", newline="", encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    store = MMapDirectory(Paths.get('index'))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)
    index_csv_data(csv_reader, writer)
    writer.commit()
    writer.close()

# user_name = input('Enter the name to search for: ')
# user_position = input("Enter the position to search for: ")
# user_nationality = input("Enter the nationality to search for: ")
# start_year = input("Enter the start year of the range: ")
# end_year = input("Enter the end year of the range: ")
# user_round = input("Enter the round: ")
# user_overall = input("Enter the overall: ")
# junior_team = input("Enter the junior_team: ")

# user_name = ""
# user_position = ""
# user_nationality = "Sk"
# user_round = ""
# user_overall = "1st"
# start_year = ""
# end_year = ""


def search_data(user_name, user_position, user_nationality, start_year, end_year,
                user_round, user_overall, junior_team):

    searcher = IndexSearcher(DirectoryReader.open(store))
    boolean_query = BooleanQuery.Builder()

    if user_name:
        name_term = Term("name", user_name)
        name_query = TermQuery(name_term)
        boolean_query.add(name_query, BooleanClause.Occur.MUST)

    if user_position:
        position_term = Term("position", user_position)
        position_query = TermQuery(position_term)
        boolean_query.add(position_query, BooleanClause.Occur.MUST)

    if user_nationality:
        nationality_term = Term("nationality", user_nationality)
        nationality_query = TermQuery(nationality_term)
        boolean_query.add(nationality_query, BooleanClause.Occur.MUST)

    if start_year and end_year:
        year_range_query = TermRangeQuery.newStringRange("year", start_year, end_year, True, True)
        boolean_query.add(year_range_query, BooleanClause.Occur.MUST)

    if user_round:
        round_term = Term("round", user_round)
        round_query = TermQuery(round_term)
        boolean_query.add(round_query, BooleanClause.Occur.MUST)

    if user_overall:
        overall_term = Term("overall", user_overall)
        overall_query = TermQuery(overall_term)
        boolean_query.add(overall_query, BooleanClause.Occur.MUST)

    if junior_team:
        junior_team_term = Term("junior_team", junior_team)
        junior_team_query = TermQuery(junior_team_term)
        boolean_query.add(junior_team_query, BooleanClause.Occur.MUST)

    results = searcher.search(boolean_query.build(), 20)  # Adjust the number of results as needed

    matching_entries = []
    for score_doc in results.scoreDocs:
        doc = searcher.doc(score_doc.doc)
        matching_entries.append({
            "Name": doc.get("name"),
            "Team": doc.get("team"),
            "Year": doc.get("year"),
            "Round": doc.get("round"),
            "Overall": doc.get("overall"),
            "Position": doc.get("position"),
            "Nationality": doc.get("nationality"),
            "Junior_team": doc.get("junior_team"),
        })

    searcher.getIndexReader().close()
    return matching_entries


class TestYourCode(unittest.TestCase):
    def test_search_bedard(self):
        user_name = "Connor Bedard"
        user_position = ""
        user_nationality = "Ca"
        start_year = "2023"
        end_year = "2023"
        user_round = "1"
        user_overall = "1"
        junior_team = ""

        # Perform the search
        results = search_data(user_name, user_position, user_nationality, start_year, end_year,
                              user_round, user_overall, junior_team)

        # Check if the expected results are present
        expected_result = [
            {
                "Name": "Connor Bedard",
                "Team": "Chicago",
                "Round": "1",
                "Overall": "1",
                "Year": "2023",
                "Position": "C",
                "Nationality": "Ca",
                "Junior_team": "Regina Pats (Western Hockey League|WHL)",
            }
        ]

        self.assertEqual(results, expected_result)

    def test_search_slaf(self):
        user_name = ""
        user_position = ""
        user_nationality = "Sk"
        start_year = "2022"
        end_year = "2022"
        user_round = "1"
        user_overall = "1"
        junior_team = ""

        # Perform the search
        results = search_data(user_name, user_position, user_nationality, start_year, end_year,
                              user_round, user_overall, junior_team)

        # Check if the expected results are present
        expected_result = [
            {
                "Name": "Juraj Slafkovsky",
                "Team": "Montreal",
                "Round": "1",
                "Overall": "1",
                "Year": "2022",
                "Position": "LW",
                "Nationality": "Sk",
                "Junior_team": "HC TPS (Liiga)",
            }
        ]

        self.assertEqual(results, expected_result)

    def test_search_name(self):
        user_name = "Brett Hyland"
        user_position = ""
        user_nationality = ""
        start_year = ""
        end_year = ""
        user_round = ""
        user_overall = ""
        junior_team = ""

        # Perform the search
        results = search_data(user_name, user_position, user_nationality, start_year, end_year,
                              user_round, user_overall, junior_team)

        # Check if the expected results are present
        expected_result = [
            {
                "Name": "Brett Hyland",
                "Team": "Washington",
                "Round": "7",
                "Overall": "200",
                "Year": "2023",
                "Position": "C",
                "Nationality": "Ca",
                "Junior_team": "Brandon Wheat Kings (WHL)",
            }
        ]

        self.assertEqual(results, expected_result)

    def test_search_sk(self):
        user_name = ""
        user_position = ""
        user_nationality = "Sk"
        start_year = "2023"
        end_year = "2023"
        user_round = "1"
        user_overall = ""
        junior_team = ""

        # Perform the search
        results = search_data(user_name, user_position, user_nationality, start_year, end_year,
                              user_round, user_overall, junior_team)

        # Check if the expected results are present
        expected_result = [
            {
                'Name': 'Dalibor Dvorsky',
                'Team': 'St. Louis',
                'Year': '2023',
                'Round': '1',
                'Overall': '10',
                'Position': 'C',
                'Nationality': 'Sk',
                'Junior_team': 'AIK IF (HockeyAllsvenskan)'
            },
            {
                'Name': 'Samuel Honzek',
                'Team': 'Calgary',
                'Year': '2023',
                'Round': '1',
                'Overall': '16',
                'Position': 'LW',
                'Nationality': 'Sk',
                'Junior_team': 'Vancouver Giants (WHL)'
            }
        ]

        self.assertEqual(results, expected_result)


if __name__ == '__main__':
    unittest.main()
