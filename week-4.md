# Running the wordcount programming asignment with Cloudera's Docker container

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


# Programming assignment on joining data
First, create the files `join1_FileA.txt`, `join1_FileB.txt`, `join1_mapper.py`, and `join1_reducer.py` (and `chmod +x` both Python scripts to make them executable). Before running the Cloudera container, we want to validate these files on the command line, i.e., without using Hadoop and its MapReduce framework. On the local host, try running:

```shell
$ cat join1_File*
able,991
about,11
burger,15
actor,22
Jan-01 able,5
Feb-02 about,3
Mar-03 about,8
Apr-04 able,13
Feb-22 actor,3
Feb-23 burger,5
Mar-08 burger,2
Dec-15 able,100
$ cat join1_File* | ./join1_mapper.py
able	991
about	11
burger	15
actor	22
able	Jan-01 5
about	Feb-02 3
about	Mar-03 8
able	Apr-04 13
actor	Feb-22 3
burger	Feb-23 5
burger	Mar-08 2
able	Dec-15 100
$ 
``` 

The mapper correctly moves the date into the value field. Now try to pipe this to the reducer:

```shell
$ cat join1_File* | ./join1_mapper.py | sort | ./join1_reducer.py 
Apr-04 able 13 991
Dec-15 able 100 991
Jan-01 able 5 991
Feb-02 about 3 11
Mar-03 about 8 11
Feb-22 actor 3 22
Feb-23 burger 5 15
Mar-08 burger 2 15
$ 
```

If anything goes wrong with the above command, you need to fix the mapper or the reducer.

To run the data joins in the Docker container, We can again use the `-v` option to access the above files within the Cloudera Docker container. But this time, to avoid passing 4 arguments to the Docker command, we'll mount the complete directory `joining-data-assignment` instead. Change into the root directory of this repository on the host machine and run:

```shell
$ docker run --hostname=quickstart.cloudera --privileged=true -p 8888:8888 -p 9000:80 -it --rm --name cloudera -v $(pwd)/joining-data-assignment:/home/cloudera/joining-data-assignment cloudera/quickstart /usr/bin/docker-quickstart
```

Next, we put the data in `join1_FileA.txt` and `join1_FileB.txt` into HDFS:

```shell
[root@quickstart /]# hdfs dfs -ls /user/cloudera
[root@quickstart /]# hdfs dfs -ls /user/
Found 8 items
drwxr-xr-x   - cloudera cloudera            0 2016-04-06 02:25 /user/cloudera
drwxr-xr-x   - mapred   hadoop              0 2016-04-06 02:26 /user/history
drwxrwxrwx   - hive     supergroup          0 2016-04-06 02:27 /user/hive
drwxrwxrwx   - hue      supergroup          0 2016-04-06 02:26 /user/hue
drwxrwxrwx   - jenkins  supergroup          0 2016-04-06 02:26 /user/jenkins
drwxrwxrwx   - oozie    supergroup          0 2016-04-06 02:27 /user/oozie
drwxrwxrwx   - root     supergroup          0 2016-04-06 02:26 /user/root
drwxr-xr-x   - hdfs     supergroup          0 2016-04-06 02:27 /user/spark
[root@quickstart /]# hdfs dfs -mkdir /user/cloudera/joining-data-input
[root@quickstart /]# hdfs dfs -ls /user/cloudera
Found 1 items
drwxr-xr-x   - root cloudera          0 2020-03-26 11:32 /user/cloudera/joining-data-input
[root@quickstart /]# hdfs dfs -put /home/cloudera/joining-data-assignment/join1_FileA.txt /user/cloudera/joining-data-input
[root@quickstart /]# hdfs dfs -put /home/cloudera/joining-data-assignment/join1_FileB.txt /user/cloudera/joining-data-input
[root@quickstart /]# hdfs dfs -ls /user/cloudera/joining-data-input
Found 2 items
-rw-r--r--   1 root cloudera         37 2020-03-26 11:32 /user/cloudera/joining-data-input/join1_FileA.txt
-rw-r--r--   1 root cloudera        122 2020-03-26 11:33 /user/cloudera/joining-data-input/join1_FileB.txt
[root@quickstart /]#
```

We will now run the Hadoop MapReduce. In the Docker container, issue:

```shell
[root@quickstart cloudera]# hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar -input /user/cloudera/joining-data-input -output /user/cloudera/joining-data-output -mapper /home/cloudera/joining-data-assignment/join1_mapper.py -reducer /home/cloudera/joining-data-assignment/join1_reducer.py
```

Check the output of MapReduce:

```shell
[root@quickstart cloudera]# hdfs dfs -ls /user/cloudera/joining-data-output
Found 2 items
-rw-r--r--   1 root cloudera          0 2020-03-26 12:40 /user/cloudera/joining-data-output/_SUCCESS
-rw-r--r--   1 root cloudera        157 2020-03-26 12:40 /user/cloudera/joining-data-output/part-00000
[root@quickstart cloudera]# hdfs dfs -cat /user/cloudera/joining-data-output/part-00000
Dec-15 able 100 991	
Apr-04 able 13 991	
Jan-01 able 5 991	
Mar-03 about 8 11	
Feb-02 about 3 11	
Feb-22 actor 3 22	
Feb-23 burger 5 15	
Mar-08 burger 2 15	
[root@quickstart cloudera]# 
```

## Part 2: A New Join Problem
Run the shell script to generate the (random) data for the new join problem:

```shell
[root@quickstart cloudera]# cd joining-data-assignment/
[root@quickstart joining-data-assignment]# ./make_data_join2.sh 
[root@quickstart joining-data-assignment]# ls
join1_FileA.txt  join1_mapper.py   join2_genchanA.txt  join2_genchanC.txt  join2_gennumB.txt  make_data_join2.sh
join1_FileB.txt  join1_reducer.py  join2_genchanB.txt  join2_gennumA.txt   join2_gennumC.txt  make_join2data.py
[root@quickstart joining-data-assignment]# 
```

Next, we put the data files `join2_*` into HDFS:

```shell
[root@quickstart joining-data-assignment]# hdfs dfs -mkdir /user/cloudera/join2-data-input
[root@quickstart joining-data-assignment]# hdfs dfs -put join2_gen* /user/cloudera/join2-data-input/
[root@quickstart joining-data-assignment]# hdfs dfs -ls /user/cloudera/join2-data-input/
Found 6 items
-rw-r--r--   1 root cloudera       1714 2020-03-26 17:07 /user/cloudera/join2-data-input/join2_genchanA.txt
-rw-r--r--   1 root cloudera       3430 2020-03-26 17:07 /user/cloudera/join2-data-input/join2_genchanB.txt
-rw-r--r--   1 root cloudera       5152 2020-03-26 17:07 /user/cloudera/join2-data-input/join2_genchanC.txt
-rw-r--r--   1 root cloudera      17114 2020-03-26 17:07 /user/cloudera/join2-data-input/join2_gennumA.txt
-rw-r--r--   1 root cloudera      34245 2020-03-26 17:07 /user/cloudera/join2-data-input/join2_gennumB.txt
-rw-r--r--   1 root cloudera      51400 2020-03-26 17:07 /user/cloudera/join2-data-input/join2_gennumC.txt
[root@quickstart joining-data-assignment]# 
```

Now, run MapReduce:

```shell
[root@quickstart joining-data-assignment]# hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar -input /user/cloudera/join2-data-input -output /user/cloudera/join2-data-output -mapper /home/cloudera/joining-data-assignment/join2_mapper.py -reducer /home/cloudera/joining-data-assignment/join2_reducer.py
...
[root@quickstart joining-data-assignment]# hdfs dfs -cat /user/cloudera/join2-data-output/part-00000
Almost_Games 49237	
Almost_News 46592	
Almost_Show 50202	
Baked_Games 51604	
Baked_News 47211	
Cold_News 47924	
Cold_Sports 52005	
Dumb_Show 53824	
Dumb_Talking 103894	
Hot_Games 50228	
Hot_Show 54378	
Hourly_Cooking 54208	
Hourly_Show 48283	
Hourly_Talking 108163	
Loud_Games 49482	
Loud_Show 50820	
PostModern_Games 50644	
PostModern_News 50021	
Surreal_News 50420	
Surreal_Sports 46834	
[root@quickstart joining-data-assignment]# 
```

Remark: I personally find the assignment question ambiguous. "What is the total number of viewers for shows on ABC?" could mean that you need to find the total number of *ABC* viewers for shows that run on ABC. Based on the correct result of the MapReduce in this exercise, it turns out that the intended question is actually: "What is the total number of viewers across all channels for shows that are aired on ABC? (these shows could be aired on other channels as well)".

To answer this question, we first need a mapper takes `<TV show, viewer count>` and `<TV show, channel>` pairs as input, and outputs `<TV show, viewer count>` pairs and `<TV show, channel>` pairs **if** channel is "ABC". In other words, the mapper will ouput pairs where the name of the TV show is the key and the viewer count or the channel the TV show is aired on is the value.  
We then need a reducer that takes pairs `<TV show, viewer count>` and `<TV show, channel>` where channel is "ABC", and outputs pairs `<TV show<space>total viewer count>` with the total viewer count (across all channels) for shows that are aired on "ABC" (and, potentially, also on other channels).

The above works because Hadoop's MapReduce sorts the mapper output like this

```
...
Almost_Cooking,980
Almost_Cooking,998
Almost_Games,1006
...
Almost_Games,996
Almost_Games,ABC
Almost_News,1003
Almost_News,101
...
```

So if we process the above mapper output line by line, keep the running total viewer count for a TV show and:
  1. the key (i.e., the TV show name) changes, and 
  2. the last pair had "ABC" as its value,

then the running total contains the sum of all viewers of this show (across all channels) and because the value of the last line (before the key changed) is "ABC", we know that this show is aired on ABC as well. Thus, we can print the pair `<TV show, total viewer count>` to answer the question: "what is the total number of viewers for shows on ABC?".
