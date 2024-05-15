# financial-strategy-experiment


# Development
```bash
python -m venv .venv
source .venv/bin/activate

jupyter lab
jupyter lab build
```

## Local installation
1. install 
    ```bash
    curl -O https://dlcdn.apache.org/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz
    tar -xzf spark-3.5.1-bin-hadoop3.tgz
    if [ ! -d "/opt/spark" ]; then
        sudo mkdir -p /opt/spark
    fi
    sudo mv spark-3.5.1-bin-hadoop3 /opt/spark
    sudo mv /opt/spark/spark-3.5.1-bin-hadoop3/* /opt/spark/
    curl -O https://repo1.maven.org/maven2/org/apache/spark/spark-hadoop-cloud_2.13/3.5.1/spark-hadoop-cloud_2.13-3.5.1.jar && sudo mv spark-hadoop-cloud_2.13-3.5.1.jar /opt/spark/jars
    ```
2. set up envs in `~/.bash_profile` or similar file.
    edit
    ```text
    # set up envs
    export SPARK_HOME=/opt/spark
    export PATH=$SPARK_HOME/bin:$PATH
    ```
    source
    ```bash
    source ~/.bash_profile
    ```
