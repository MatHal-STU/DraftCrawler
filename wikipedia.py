from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import re

spark = SparkSession.builder.appName("wikipedia").getOrCreate()
result_df = spark.createDataFrame([], 'Overall STRING, Name STRING, Junior_Team STRING, Country STRING, Year String')
columns = ["Overall", "Name", "Country", "Junior_Team", "Year"]


def extract_all(text):
    rows = []
    pattern = '! (\d+\s*)\\n\| ([\s\S]*?)\\n\| {{flagicon\|.*?}} ([\s\S]*?)\\n\|[\s\S]*?\\n\|([\s\S]*?)\\n'
    pattern2= '! (\d+\s*)\\n\| ([\s\S]*?)\\n\| {{(.*?)}}\\n\| [\s\S]*?\\n\| ([\s\S]*?)\\n'
    matches = re.findall(pattern, text)
    if not matches:
        matches = re.findall(pattern2, text)
    for match in matches:
        country = match[2]
        name = match[1]
        overall = match[0]
        name = re.sub(r'bgcolor=[^|]*\| ', '', name)
        name = re.sub(r'\(.*?\)', '', name)
        name = re.sub(r'\(.*?\)', '', name)
        name = re.sub(r'\| .+$', '', name)
        name = re.sub(r'\|.*$', '', name)
        name = re.sub(r'^ ', '', name)
        name = name.replace("[[", "")
        name = name.replace("]]", "")
        overall = overall.replace(" ", "")
        team = match[3]
        team = team.replace("[[", "")
        team = team.replace("]]", "")

        rows.append([overall, name, country, team])

    if rows:
        return rows
    else:
        return None


if __name__ == "__main__":
    xml_file_path = "D:\\Skola\\VINF\\DraftCrawler\\wiki\\enwiki-latest-pages-articles10.xml"

    df = spark.read.option("rowTag", "page").format("xml").load(xml_file_path)
    df_filtered = df.filter(df.title.rlike('(\d{4})(?i) NHL Entry Draft'))
    if df_filtered:
        df_select = df_filtered.select("revision.text._VALUE", "title")
        extract_all_udf = udf(lambda z: extract_all(z), ArrayType(ArrayType(StringType())))
        df_result_names = df_select.withColumn("extracted_names", extract_all_udf(col("_VALUE")))
        df_result_names.select("title","extracted_names").show(truncate=False)
        df_result_names = df_result_names.select("extracted_names", "title")
        data_collect = df_result_names.collect()

        for row in data_collect:
            year = re.search('(\d{4})', row["title"]).group(1).strip()
            daco = row["extracted_names"]
            if daco:
                for i in daco:
                    i.append(year)
                help_df = spark.createDataFrame(daco, columns)
                result_df = result_df.unionByName(help_df)

    result_df.write.csv("D:\\Skola\\VINF\\DraftCrawler\\wiki\\result")

    spark.stop()

# \| \[\[(.*?)\]\] \((.*?)\)\n\| {{flagicon\|(.*?)}}
# \|  \[\[(.*?)\]\] \((.*?)\)\n\| {{flagicon\|(.*?)}}
# ^! \d+\s*\| .+$
# ! \d+\s*\\n\| ([\s\S]*?\\n)
# ! (\d+\s *)\ |  \[\[(.* ?)\]\] \((.* ?)\)\n\ | {{flagicon\ | (.* ?)}}
# ^! (\d+\s*)\\n\| (.+$)\\n\| {{flagicon\|(.* ?)}}.+$\\n\|.+$\\n\|(.+$)
