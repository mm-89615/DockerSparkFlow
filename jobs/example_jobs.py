from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ExampleJob").getOrCreate()

data = [("Alice", 29), ("Bob", 31), ("Cathy", 25)]
df = spark.createDataFrame(data, ["name", "age"])
df.show()

spark.stop()
