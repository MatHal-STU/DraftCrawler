from pyspark.sql import SparkSession
from pyspark.sql.functions import *

if __name__ == "__main__":
    spark = SparkSession \
        .builder\
        .master("local[*]")\
        .appName("wikipedia")\
        .getOrCreate()

    lines = spark.read.text('./file.txt')

    wordcounts = lines.select(explode(split(lines.value, "\s+"))
                .alias("word")) \
        .groupby("word") \
        .count()
    print("\n Word count: ", wordcounts.show(20,5))

    spark.stop()
