# Installing IPython
Since we use a Docker image instead of the virtual machine, we run the existing `cloudera/quickstart` Docker image, install IPython, and use the `docker commit` command to create a new image from the container's changes. This way, we can create a new Docker image that contains everything in `cloudera/quickstart` as well as our changes (i.e., the IPython installation).

To install IPython, start the Docker container:

```shell
$ docker run --hostname=quickstart.cloudera --privileged=true -p 8888:8888 -p 9000:80 -it --rm --name cloudera -v $(pwd)/spark-assignment:/home/cloudera/spark-assigment cloudera/quickstart /usr/bin/docker-quickstart
```

The Cloudera's Docker image uses CentOS 6.6 as its operating system:

```shell
[root@quickstart /]# lsb_release -sirc
CentOS 6.6 Final
[root@quickstart /]# 
``` 
CentOS uses `yum` to install new packages (the `easy_install` tool doesn't work for the Docker container, probably due to [this bug](https://bugzilla.redhat.com/show_bug.cgi?id=1510444)). We already downloaded the ipython rpm package and mounted it under `/home/cloudera/spark-assignment`. Thus, we can now simply issue:

```shell
[root@quickstart /]# cd /home/cloudera/
[root@quickstart cloudera]# ls
cloudera-manager  cm_api.py  Desktop  Documents  enterprise-deployment.json  express-deployment.json  kerberos  lib  parcels  spark-assigment  workspace
[root@quickstart cloudera]# cd spark-assigment/
[root@quickstart cloudera]# yum install ipython
...
Total download size: 63 M
Is this ok [y/N]: y
Downloading Packages:
...
Running rpm_check_debug
Running Transaction Test
Transaction Test Succeeded
Running Transaction
  Installing : ... 
...
[root@quickstart spark-assigment]#
```

We can now run `pyspark`:

```shell
[root@quickstart spark-assigment]# export PYSPARK_DRIVER_PYTHON=ipython
[root@quickstart spark-assigment]# pyspark
Python 2.6.6 (r266:84292, Jul 23 2015, 15:22:56) 
Type "copyright", "credits" or "license" for more information.

IPython 0.13.2 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.

In [1]:
```

In the pyspakt shell, type

```shell
In [7]: from pyspark import SparkContext

In [8]: sc = SparkContext()
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/usr/lib/zookeeper/lib/slf4j-log4j12-1.7.5.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/usr/jars/slf4j-log4j12-1.7.5.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.slf4j.impl.Log4jLoggerFactory]
20/04/09 20:39:20 INFO spark.SparkContext: Running Spark version 1.6.0
20/04/09 20:39:20 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
20/04/09 20:39:20 INFO spark.SecurityManager: Changing view acls to: root
20/04/09 20:39:20 INFO spark.SecurityManager: Changing modify acls to: root
20/04/09 20:39:20 INFO spark.SecurityManager: SecurityManager: authentication disabled; ui acls disabled; users with view permissions: Set(root); users with modify permissions: Set(root)
20/04/09 20:39:21 INFO util.Utils: Successfully started service 'sparkDriver' on port 44445.
20/04/09 20:39:21 INFO slf4j.Slf4jLogger: Slf4jLogger started
20/04/09 20:39:21 INFO Remoting: Starting remoting
20/04/09 20:39:21 INFO Remoting: Remoting started; listening on addresses :[akka.tcp://sparkDriverActorSystem@172.17.0.2:45777]
20/04/09 20:39:21 INFO Remoting: Remoting now listens on addresses: [akka.tcp://sparkDriverActorSystem@172.17.0.2:45777]
20/04/09 20:39:21 INFO util.Utils: Successfully started service 'sparkDriverActorSystem' on port 45777.
20/04/09 20:39:21 INFO spark.SparkEnv: Registering MapOutputTracker
20/04/09 20:39:21 INFO spark.SparkEnv: Registering BlockManagerMaster
20/04/09 20:39:21 INFO storage.DiskBlockManager: Created local directory at /tmp/blockmgr-e0f577f0-8508-4677-a28e-bdbd905a2b01
20/04/09 20:39:21 INFO storage.MemoryStore: MemoryStore started with capacity 530.3 MB
20/04/09 20:39:21 INFO spark.SparkEnv: Registering OutputCommitCoordinator
20/04/09 20:39:21 INFO server.Server: jetty-8.y.z-SNAPSHOT
20/04/09 20:39:21 INFO server.AbstractConnector: Started SelectChannelConnector@0.0.0.0:4040
20/04/09 20:39:21 INFO util.Utils: Successfully started service 'SparkUI' on port 4040.
20/04/09 20:39:21 INFO ui.SparkUI: Started SparkUI at http://172.17.0.2:4040
20/04/09 20:39:21 INFO executor.Executor: Starting executor ID driver on host localhost
20/04/09 20:39:21 INFO util.Utils: Successfully started service 'org.apache.spark.network.netty.NettyBlockTransferService' on port 46453.
20/04/09 20:39:21 INFO netty.NettyBlockTransferService: Server created on 46453
20/04/09 20:39:21 INFO storage.BlockManagerMaster: Trying to register BlockManager
20/04/09 20:39:21 INFO storage.BlockManagerMasterEndpoint: Registering block manager localhost:46453 with 530.3 MB RAM, BlockManagerId(driver, localhost, 46453)
20/04/09 20:39:21 INFO storage.BlockManagerMaster: Registered BlockManager

In [9]: integer_RDD = sc.parallelize(range(10),3)

In [10]: integer_RDD.collect()
20/04/09 20:41:51 INFO spark.SparkContext: Starting job: collect at <ipython-input-10-bacea4515bc8>:1
20/04/09 20:41:51 INFO scheduler.DAGScheduler: Got job 0 (collect at <ipython-input-10-bacea4515bc8>:1) with 3 output partitions
20/04/09 20:41:51 INFO scheduler.DAGScheduler: Final stage: ResultStage 0 (collect at <ipython-input-10-bacea4515bc8>:1)
20/04/09 20:41:51 INFO scheduler.DAGScheduler: Parents of final stage: List()
20/04/09 20:41:51 INFO scheduler.DAGScheduler: Missing parents: List()
20/04/09 20:41:51 INFO scheduler.DAGScheduler: Submitting ResultStage 0 (ParallelCollectionRDD[0] at parallelize at PythonRDD.scala:423), which has no missing parents
20/04/09 20:41:51 INFO storage.MemoryStore: Block broadcast_0 stored as values in memory (estimated size 1224.0 B, free 1224.0 B)
20/04/09 20:41:51 INFO storage.MemoryStore: Block broadcast_0_piece0 stored as bytes in memory (estimated size 777.0 B, free 2001.0 B)
20/04/09 20:41:51 INFO storage.BlockManagerInfo: Added broadcast_0_piece0 in memory on localhost:46453 (size: 777.0 B, free: 530.3 MB)
20/04/09 20:41:51 INFO spark.SparkContext: Created broadcast 0 from broadcast at DAGScheduler.scala:1006
20/04/09 20:41:51 INFO scheduler.DAGScheduler: Submitting 3 missing tasks from ResultStage 0 (ParallelCollectionRDD[0] at parallelize at PythonRDD.scala:423)
20/04/09 20:41:51 INFO scheduler.TaskSchedulerImpl: Adding task set 0.0 with 3 tasks
20/04/09 20:41:51 INFO scheduler.TaskSetManager: Starting task 0.0 in stage 0.0 (TID 0, localhost, partition 0,PROCESS_LOCAL, 2088 bytes)
20/04/09 20:41:51 INFO scheduler.TaskSetManager: Starting task 1.0 in stage 0.0 (TID 1, localhost, partition 1,PROCESS_LOCAL, 2088 bytes)
20/04/09 20:41:51 INFO scheduler.TaskSetManager: Starting task 2.0 in stage 0.0 (TID 2, localhost, partition 2,PROCESS_LOCAL, 2107 bytes)
20/04/09 20:41:51 INFO executor.Executor: Running task 0.0 in stage 0.0 (TID 0)
20/04/09 20:41:51 INFO executor.Executor: Running task 1.0 in stage 0.0 (TID 1)
20/04/09 20:41:51 INFO executor.Executor: Running task 2.0 in stage 0.0 (TID 2)
20/04/09 20:41:51 INFO executor.Executor: Finished task 2.0 in stage 0.0 (TID 2). 955 bytes result sent to driver
20/04/09 20:41:51 INFO executor.Executor: Finished task 0.0 in stage 0.0 (TID 0). 936 bytes result sent to driver
20/04/09 20:41:51 INFO executor.Executor: Finished task 1.0 in stage 0.0 (TID 1). 936 bytes result sent to driver
20/04/09 20:41:51 INFO scheduler.TaskSetManager: Finished task 0.0 in stage 0.0 (TID 0) in 66 ms on localhost (1/3)
20/04/09 20:41:51 INFO scheduler.TaskSetManager: Finished task 2.0 in stage 0.0 (TID 2) in 44 ms on localhost (2/3)
20/04/09 20:41:51 INFO scheduler.TaskSetManager: Finished task 1.0 in stage 0.0 (TID 1) in 45 ms on localhost (3/3)
20/04/09 20:41:51 INFO scheduler.TaskSchedulerImpl: Removed TaskSet 0.0, whose tasks have all completed, from pool 
20/04/09 20:41:51 INFO scheduler.DAGScheduler: ResultStage 0 (collect at <ipython-input-10-bacea4515bc8>:1) finished in 0.078 s
20/04/09 20:41:51 INFO scheduler.DAGScheduler: Job 0 finished: collect at <ipython-input-10-bacea4515bc8>:1, took 0.206092 s
Out[10]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
In [11]: integer_RDD.glom().collect()
20/04/09 20:43:11 INFO spark.SparkContext: Starting job: collect at <ipython-input-11-7b85bb20a109>:1
20/04/09 20:43:11 INFO scheduler.DAGScheduler: Got job 1 (collect at <ipython-input-11-7b85bb20a109>:1) with 3 output partitions
20/04/09 20:43:11 INFO scheduler.DAGScheduler: Final stage: ResultStage 1 (collect at <ipython-input-11-7b85bb20a109>:1)
20/04/09 20:43:11 INFO scheduler.DAGScheduler: Parents of final stage: List()
20/04/09 20:43:11 INFO scheduler.DAGScheduler: Missing parents: List()
20/04/09 20:43:11 INFO scheduler.DAGScheduler: Submitting ResultStage 1 (PythonRDD[1] at collect at <ipython-input-11-7b85bb20a109>:1), which has no missing parents
20/04/09 20:43:11 INFO storage.MemoryStore: Block broadcast_1 stored as values in memory (estimated size 3.2 KB, free 5.2 KB)
20/04/09 20:43:11 INFO storage.MemoryStore: Block broadcast_1_piece0 stored as bytes in memory (estimated size 2.1 KB, free 7.3 KB)
20/04/09 20:43:11 INFO storage.BlockManagerInfo: Added broadcast_1_piece0 in memory on localhost:46453 (size: 2.1 KB, free: 530.3 MB)
20/04/09 20:43:11 INFO spark.SparkContext: Created broadcast 1 from broadcast at DAGScheduler.scala:1006
20/04/09 20:43:11 INFO scheduler.DAGScheduler: Submitting 3 missing tasks from ResultStage 1 (PythonRDD[1] at collect at <ipython-input-11-7b85bb20a109>:1)
20/04/09 20:43:11 INFO scheduler.TaskSchedulerImpl: Adding task set 1.0 with 3 tasks
20/04/09 20:43:11 INFO scheduler.TaskSetManager: Starting task 0.0 in stage 1.0 (TID 3, localhost, partition 0,PROCESS_LOCAL, 2088 bytes)
20/04/09 20:43:11 INFO scheduler.TaskSetManager: Starting task 1.0 in stage 1.0 (TID 4, localhost, partition 1,PROCESS_LOCAL, 2088 bytes)
20/04/09 20:43:11 INFO scheduler.TaskSetManager: Starting task 2.0 in stage 1.0 (TID 5, localhost, partition 2,PROCESS_LOCAL, 2107 bytes)
20/04/09 20:43:11 INFO executor.Executor: Running task 0.0 in stage 1.0 (TID 3)
20/04/09 20:43:11 INFO executor.Executor: Running task 1.0 in stage 1.0 (TID 4)
20/04/09 20:43:11 INFO executor.Executor: Running task 2.0 in stage 1.0 (TID 5)
20/04/09 20:43:11 INFO python.PythonRunner: Times: total = 159, boot = 149, init = 10, finish = 0
20/04/09 20:43:11 INFO executor.Executor: Finished task 0.0 in stage 1.0 (TID 3). 1004 bytes result sent to driver
20/04/09 20:43:11 INFO python.PythonRunner: Times: total = 163, boot = 149, init = 14, finish = 0
20/04/09 20:43:11 INFO scheduler.TaskSetManager: Finished task 0.0 in stage 1.0 (TID 3) in 177 ms on localhost (1/3)
20/04/09 20:43:11 INFO executor.Executor: Finished task 2.0 in stage 1.0 (TID 5). 1006 bytes result sent to driver
20/04/09 20:43:11 INFO python.PythonRunner: Times: total = 172, boot = 160, init = 12, finish = 0
20/04/09 20:43:11 INFO scheduler.TaskSetManager: Finished task 2.0 in stage 1.0 (TID 5) in 180 ms on localhost (2/3)
20/04/09 20:43:11 INFO executor.Executor: Finished task 1.0 in stage 1.0 (TID 4). 1004 bytes result sent to driver
20/04/09 20:43:11 INFO scheduler.TaskSetManager: Finished task 1.0 in stage 1.0 (TID 4) in 185 ms on localhost (3/3)
20/04/09 20:43:11 INFO scheduler.TaskSchedulerImpl: Removed TaskSet 1.0, whose tasks have all completed, from pool 
20/04/09 20:43:11 INFO scheduler.DAGScheduler: ResultStage 1 (collect at <ipython-input-11-7b85bb20a109>:1) finished in 0.188 s
20/04/09 20:43:11 INFO scheduler.DAGScheduler: Job 1 finished: collect at <ipython-input-11-7b85bb20a109>:1, took 0.203094 s
Out[11]: [[0, 1, 2], [3, 4, 5], [6, 7, 8, 9]]
```



