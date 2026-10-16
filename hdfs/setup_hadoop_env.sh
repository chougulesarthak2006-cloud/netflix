#!/usr/bin/env bash
# ==============================================================================
# Script Name: setup_hadoop_env.sh
# Description: Helper script to verify and display Hadoop and Hive environment
#              variables for Ubuntu / Linux single-node clusters.
# ==============================================================================

echo "==================================================================="
echo "       Hadoop & Hive Environment Configuration Checker            "
echo "==================================================================="

# Standard default paths on Ubuntu
DEFAULT_JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"
if [ ! -d "$DEFAULT_JAVA_HOME" ]; then
    DEFAULT_JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"
fi

echo "Current Environment Variables:"
echo "-------------------------------------------------------------------"
echo "JAVA_HOME:    ${JAVA_HOME:-[NOT SET] (Suggested: $DEFAULT_JAVA_HOME)}"
echo "HADOOP_HOME:  ${HADOOP_HOME:-[NOT SET] (Suggested: /usr/local/hadoop or /opt/hadoop)}"
echo "HIVE_HOME:    ${HIVE_HOME:-[NOT SET] (Suggested: /usr/local/hive or /opt/hive)}"
echo "PATH:         $PATH"
echo "-------------------------------------------------------------------"

echo ""
echo "If any of these are not set, append the following block to your ~/.bashrc:"
echo ""
cat << 'EOF'
# --- Hadoop & Hive Environment Variables ---
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export HADOOP_HOME=/usr/local/hadoop
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export HIVE_HOME=/usr/local/hive

export PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$HIVE_HOME/bin
# -------------------------------------------
EOF

echo ""
echo "Then apply the changes by running:"
echo "  source ~/.bashrc"
echo "==================================================================="
