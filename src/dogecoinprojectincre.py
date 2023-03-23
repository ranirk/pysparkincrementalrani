import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.functions import col
from pyspark.sql.functions import lit

from pyspark.sql.functions import col
from pyspark.sql import functions as F
from pyspark.sql.functions import concat,concat_ws


spark = SparkSession.builder.master("local").appName("PySpark_Postgres_test").getOrCreate()
dburl="jdbc:postgresql://ec2-13-40-49-105.eu-west-2.compute.amazonaws.com:5432/testdb"

max = spark.sql("select max(coin_id) from pythongroup.dogecoinproject as max")

max = max.first()['max(coin_id)']

query="(select * from dogecoinproject where coin_id >"+str(max)+ ") as tb"
df = spark.read.format("jdbc").option("url",dburl) \
    .option("driver", "org.postgresql.Driver").option("dbtable", query) \
    .option("user", "consultants").option("password", "WelcomeItc@2022").load()

print(df.show())

filtered_df = df.filter(col("total_volume") > 500000)
filtered_df.show()

# Create Hive Internal table
filtered_df.write.mode('append') \
    .saveAsTable("pythongroup.dogecoinproject")