# HDFS Architecture
Files are stored across different DataNodes in fixed-size (?) blocks. The MapReduce approach works as local at the data as possible. The blocks are replicated as part of the read/write process of the HDFS client. The NameNode keeps the information about where the data blocks are located, their status, etc. and it controls the DataNodes. In HDFS2, there can be multiple namespaces. 

# MapReduce
A software framework for writing parallel data processing applications:

1. split data into chunks
2. process the data chunks using "Map" tasks 
3. use (sorted) map output as input for the "Reduce" tasks

# Yarn
Resource management and scheduling: separates resource management (high-availability ResourceManager and NodeManager on each node) and job scheduling/monitoring (ApplicationMaster for each application, performs the actual MapReduce).  

# Tez
Unlike the traditional MapReduce where the data needs to be loaded from the disk every time it is processed, the newer frameworks like Yarn, Tez and Spark allow in-memory caching of data. This is especially useful (in terms of performance) when you want to analyze data interactively or when the task at hand needs to access the data iteratively, e.g., like in machine learning applications. 

# Flaw in the "Introduction to Apache Pig" Video?
At least if you use Cloudera's `cloudera/quickstart` Docker image and try to execute the commands shown in the "Introduction to Apache Pig" video from week 2, there seems to be a flaw in there. Specifically, The command `store B into 'userinfo.out'` stores the `userinfo.out` file **not** under `/user/cloudera/` but rather under `/user/root/` in HDFS. So if you exit `grunt`, the Apache Pig interactive shell, and run `hdfs dfs -ls /user/cloudera/` you won't see the `userinfo.out` file in contrast to what is shown in the video. To see it, you must `ls` into the `/user/root/directory`: execute `hdfs dfs -ls /user/root/`.
