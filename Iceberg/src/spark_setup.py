from pyspark.sql import SparkSession

def get_spark():
    spark = (
        SparkSession.builder
        .appName("IcebergApp")
        .config("spark.jars.packages", "org.apache.iceberg:iceberg-spark-runtime-3.3_2.12:1.4.2")
        .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog")
        .config("spark.sql.catalog.local.type", "hadoop")
        .config("spark.sql.catalog.local.warehouse", "C:\iceberg_data\warehouse")
        .config("spark.sql.catalog.local.io-impl", "org.apache.iceberg.hadoop.HadoopFileIO")
        .config("spark.driver.extraClassPath", "/path/to/iceberg-spark-runtime-3.3_2.12-1.4.2.jar")
        .config("spark.executor.extraClassPath", "/path/to/iceberg-spark-runtime-3.3_2.12-1.4.2.jar")
        .getOrCreate()
    )
    return spark
