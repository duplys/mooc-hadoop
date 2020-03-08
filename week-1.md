# Tools in the Cloudera Hadoop Stack
## Sqoop
Loads relational data from a MySQL database into the Hadoop Distributed File System (HDFS).

## Hive
Apacha Hive provides an SQL-like interface for reading, writing, and managing large datasets residing in distributed storage, e.g., in HDFS, using SQL. Structure can be projected onto data already in storage. See the [Wikipedia article](https://en.wikipedia.org/wiki/Apache_Hive) or the [official Hive website](https://hive.apache.org/) for more details.

## Impala
Apache Impala is a massively parallel processing (MPP) SQL query engine that runs on Apache Hadoop. Impala allows users to issue low-latency SQL queries to data stored in HDFS and Apache HBase without requiring data movement or transformation. See the [Wikipedia article](https://en.wikipedia.org/wiki/Apache_Impala) or the [official Impala website](https://impala.apache.org/) for more details. 

## Hive vs Impala
Both Hive and Impala can be used to perform similar task of querying HDFS (and databases in similar formarts). Due to their implementation details, there are various trade-offs between the two tools, e.g., speed, scalability, optimizations during compile-time vs during run-time, optimizations for batch-style vs interactive usage, etc. See [this article](https://data-flair.training/blogs/impala-vs-hive/) for more details.
