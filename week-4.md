#Running the wordcount programming asignment with Cloudera's Docker container

You can create the `wordcount_mapper.py` and `wordcount_reducer.py` files on your host machine and make them executable by issuing (still on your host machine):

```shell
$ chmod +x wordcount_mapper.py wordcount_reducer.py
``` 

To use these files within the Cloudera Docker container, use the `-v` option to mount them into the container. Change into the directory containing the Python files on the host machine and issue:

```shell
$ docker run --hostname=quickstart.cloudera --privileged=true -p 8888:8888 -p 9000:80 -it --rm --name cloudera -v $(pwd)/wordcount_mapper.py:/home/cloudera/wordcount_mapper.py -v $(pwd)/wordcount_reducer.py:/home/cloudera/wordcount_reducer.py cloudera/quickstart /usr/bin/docker-quickstart
```

Within the Docker container, create some data: 

```shell
[root@quickstart /]# echo "A long time ago in a galaxy far far away" > /home/cloudera/testfile1
[root@quickstart /]# echo "Another episode of Star Wars" > /home/cloudera/testfile2
[root@quickstart /]#
```

Next, create a new directory in the HDFS filesystem:

```shell
[root@quickstart /]# hdfs dfs -mkdir /user/cloudera/wordcount_input
[root@quickstart /]# hdfs dfs -ls /user/cloudera
Found 1 items
drwxr-xr-x   - root cloudera          0 2020-03-21 13:17 /user/cloudera/wordcount_input
[root@quickstart /]# 
``` 

Copy the data files from the local filesystem into HDFS:

```shell
[root@quickstart /]# hdfs dfs -put /home/cloudera/testfile1 /user/cloudera/wordcount_input
[root@quickstart /]# hdfs dfs -put /home/cloudera/testfile2 /user/cloudera/wordcount_input
[root@quickstart /]# hdfs dfs -ls /user/cloudera/wordcount_input/
Found 2 items
-rw-r--r--   1 root cloudera         41 2020-03-21 13:19 /user/cloudera/wordcount_input/testfile1
-rw-r--r--   1 root cloudera         95 2020-03-21 13:19 /user/cloudera/wordcount_input/testfile2
[root@quickstart /]# 
```
Run MapReduce by issuing:

```shell
[root@quickstart /]# hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar -input /user/cloudera/wordcount_input -output /user/cloudera/wordcount_output -mapper /home/cloudera/wordcount_mapper.py -reducer /home/cloudera/wordcount_reducer.py
```
You should get a lot of output now including the information on the completion status of the mapreduce job.

Run `cat` on the output file to see the results:
```shell
[root@quickstart /]# hdfs dfs -ls /user/cloudera/wordcount_output/
Found 2 items
-rw-r--r--   1 root cloudera          0 2020-03-21 13:23 /user/cloudera/wordcount_output/_SUCCESS
-rw-r--r--   1 root cloudera        138 2020-03-21 13:23 /user/cloudera/wordcount_output/part-00000
[root@quickstart /]# hdfs dfs -cat /user/cloudera/wordcount_output/part-00000
A	1
Another	1
Stars	1
Wars	1
a	3
ago	2
away	1
episode	1
far	3
galaxy	2
happened	1
in	2
long	2
of	1
story	1
telling	1
that	1
time	2
very	1
[root@quickstart /]# 
```

Finally, to run the same MapReduce job without reducers, issue:

```shell
[root@quickstart /]# hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar -input /user/cloudera/wordcount_input -output /user/cloudera/wordcount_output_without_reducer -mapper /home/cloudera/wordcount_mapper.py -reducer /home/cloudera/wordcount_reducer.py -numReduceTasks 0
```

 The following command takes a source directory and a destination file as input, and concatenates files in src into the destination local file:

```shell
[root@quickstart /]# hdfs dfs -getmerge /user/cloudera/wordcount_output_without_reducer/* wordcount_output_wo_reducer.txt
[root@quickstart /]# cat wordcount_output_wo_reducer.txt 
Another	1
episode	1
of	1
Stars	1
Wars	1
telling	1
a	1
story	1
that	1
happened	1
in	1
a	1
far	1
galaxy	1
very	1
long	1
time	1
ago	1
A	1
long	1
time	1
ago	1
in	1
a	1
galaxy	1
far	1
far	1
away	1
[root@quickstart /]# 
```

Now compare this output with the previous one.

# Helpful Commands

To quickly test the mapper outside of MapReduce and HDFS, use:

```shell
$ cat testfile1 | ./ your-mapper-program.py | sort
```

If you see the expected output, the mapper is working.

To quickly test both the mapper and the reducer outside of MapReduce and HDFS, issue:

```shell
$ cat testfile* | ./ your-mapper-program.py | sort | ./ your-reducer-program.py
```

If both mapper and reducer work as expected, you should see all the `<word, total count>` pairs. If this check passes, you can try running in this MapReduce job in Hadoop. 
