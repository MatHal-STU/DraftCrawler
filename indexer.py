import lucene
import csv

from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, TextField, StringField
from org.apache.lucene.index import IndexOptions, IndexWriter, IndexWriterConfig, DirectoryReader, Term
from org.apache.lucene.queryparser.classic import QueryParser
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
        index_writer.addDocument(doc)


with open("output.csv", "r", newline="", encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    store = MMapDirectory(Paths.get('index'))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)
    index_csv_data(csv_reader, writer)
    writer.commit()
    writer.close()

user_name = ""
user_position = ""
user_nationality = "Sk"
user_round = ""
user_overall = "1st"
start_year = ""
end_year = ""

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

results = searcher.search(boolean_query.build(), 10)  # Adjust the number of results as needed
# Print the matching entries
for score_doc in results.scoreDocs:
    doc = searcher.doc(score_doc.doc)
    print("Name: {}, Team: {}, Year: {}, Round: {}, Overall: {}, Position: {}, Nationality: {}".format(
        doc.get("name"), doc.get("team"), doc.get("year"), doc.get("round"), doc.get("overall"), doc.get("position"),
        doc.get("nationality")
    ))
