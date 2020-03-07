# Installing the Cloudera Hadoop Stack
The course video recommends to install the Cloudera VM. As an alternative, it's also possible to pull Cloudera's Docker image with the equivalent installation of the Hadoop stack:

```shell
$ docker pull cloudera/quickstart
```

Start the Docker container by issuing:

```shell
$ docker run --hostname=quickstart.cloudera --privileged=true -p 8888:8888 -it cloudera/quickstart /usr/bin/docker-quickstart
```
The option `--hostname=quickstart.cloudera` is required because the pseudo-distributed configuration assumes this hostname. Various tools in the Hadoop stack (HBase, Hive, Hue, Oozie, etc.) require the option `--privileged=true`. The `-p 8888:8888` option maps the Hue port 8888 in the Docker container to the port 8888 on the host machine (Cloudera's Docker image documentation recommendeds to use this option). Finally, the `-it` options makes the container run in the interactive mode and passes the control to the terminal.

Optionally, you can also map other ports from Cloudera's container. For instance, port 7180 gives you access to the Cloudera Manager and port 80 gives you access to a guided tour.

After the container starts, it runs `/usr/bin/docker-quickstart`. This is provided as a convenience to start all CDH services, then run a Bash shell. To start services manually, run `/bin/bash` instead.
