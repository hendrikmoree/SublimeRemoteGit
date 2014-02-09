## begin license ##
#
# All rights reserved.
#
# Copyright (C) 2013-2014 Seecr (Seek You Too B.V.) http://seecr.nl
#
## end license ##

PROJECT_DIR=$1
shift

PROJECT_NAME=$(basename "$PROJECT_DIR")
mountPoint=$PROJECT_DIR
serverProjectDir=.

while true; do
    if mount | grep "$mountPoint" > /dev/null 2>&1; then
        break
    fi
    if [ "$mountPoint" == "/" ] || [ "$mountPoint" == "." ]; then
        exit 1
    fi
    serverProjectDir=$(basename "$mountPoint")/$serverProjectDir
    mountPoint=$(dirname "$mountPoint")
done
if [ "$mountPoint" == "/" ] || [ "$mountPoint" == "." ] || [ "$mountPoint" == "$HOME/development" ]; then
    "$@"
    exit
fi
SERVER_DIR=$(mount | grep $mountPoint | awk '{print $1}' | awk -F: '{print $2}' | head -n 1)
SERVER_LOGIN=$(ps aux | grep sshfs | grep $mountPoint | awk '{print $(NF-1)}' | awk -F: '{print $1}' | head -n 1)
SERVER_PORT=$(ps aux | grep sshfs | grep $mountPoint | awk '{print $(NF-2)}' | head -n 1)
# echo REMOTE_USERNAME=${USER} ssh $SERVER_LOGIN -o SendEnv=REMOTE_USERNAME -p $SERVER_PORT "(cd $SERVER_DIR/$serverProjectDir; $args)"
REMOTE_USERNAME=${USER} ssh $SERVER_LOGIN -o SendEnv=REMOTE_USERNAME -p $SERVER_PORT "(cd $SERVER_DIR/$serverProjectDir; $@)"