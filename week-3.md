# Misc
Create a 1 GB file of random data:

```shell
$ dd if=/dev/urandom of=sample.txt bs=64M count=32
```

# `hdfs-site.xml`
At least in the Cloudera `quickstart` Docker image, the file `hdfs-site.xml` is located in:

```shell
[root@quickstart /]# ls /etc/hadoop/conf
core-site.xml  hadoop-env.sh  hadoop-metrics.properties  hdfs-site.xml  log4j.properties  mapred-site.xml  README  yarn-site.xml
```

