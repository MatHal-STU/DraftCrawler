import lucene
import csv

from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, TextField, StringField
from org.apache.lucene.index import IndexOptions, IndexWriter, IndexWriterConfig, DirectoryReader, Term
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import MMapDirectory
from org.apache.lucene.search import IndexSearcher


lucene.initVM(vmargs=['-Djava.awt.headless=true'])

def index_csv_data(csv_data, index_writer):
    for row in csv_data:
        doc = Document()
        doc.add(StringField("name", row[0], Field.Store.YES))
        doc.add(StringField("team", row[1], Field.Store.YES))
        doc.add(StringField("round", row[2], Field.Store.YES))
        doc.add(StringField("overall", row[3], Field.Store.YES))
        doc.add(StringField("year", row[4], Field.Store.YES))
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

searcher = IndexSearcher(DirectoryReader.open(store))
query_parser = QueryParser("round", analyzer)
query = query_parser.parse("1st")

results = searcher.search(query, 10)  # Adjust the number of results as needed

# Print the matching entries
for score_doc in results.scoreDocs:
    doc = searcher.doc(score_doc.doc)
    print("Name: {}, Team: {}, Year: {}".format(doc.get("name"), doc.get("team"), doc.get("year")))