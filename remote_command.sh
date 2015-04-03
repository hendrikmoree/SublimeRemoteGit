PROJECT_DIR=$1
shift
GIT_COMMAND=$1
shift

COMMAND=$GIT_COMMAND
if [ "$#" -eq "1" ]; then
    COMMAND="$COMMAND \"$1\""
fi
PROJECT_NAME=$(basename "$PROJECT_DIR")
mountPoint=$PROJECT_DIR
serverProjectDir=.
while true; do
    if mount | grep -i "$mountPoint" > /dev/null 2>&1; then
        break
    fi
    if [ "$mountPoint" == "/" ] || [ "$mountPoint" == "." ]; then
        exit 1
    fi
    serverProjectDir=$(basename "$mountPoint")/$serverProjectDir
    mountPoint=$(dirname "$mountPoint")
done
if [ "$mountPoint" == "/" ] || [ "$mountPoint" == "." ] || [ "$mountPoint" == "$HOME/development" ] || [ "$mountPoint" == "$HOME/Development" ] || [ "$mountPoint" == "$HOME" ]; then
    (
        cd "$PROJECT_DIR"
        eval $COMMAND 2>&1
    )
    exit
fi
sshfsCommand=$(ps aux | grep sshfs | grep -i $mountPoint | awk -F'sshfs' '{print $2}' | head -n 1)
SERVER_DIR=$(mount | grep -i $mountPoint | awk '{print $1}' | awk -F: '{print $2}' | head -n 1)
SERVER_LOGIN=$(echo $sshfsCommand | awk '{print $(NF-1)}' | awk -F: '{print $1}')
SERVER_PORT=22
if $(echo $sshfsCommand | grep " \-p" > /dev/null); then
    SERVER_PORT=$(echo $sshfsCommand | awk -F' -p' '{print $2}' | awk '{print $1}')
fi
# echo REMOTE_USERNAME=${USER} ssh $SERVER_LOGIN -o SendEnv=REMOTE_USERNAME -p $SERVER_PORT "(cd $SERVER_DIR/$serverProjectDir; $COMMAND)"
REMOTE_USERNAME=${USER} ssh $SERVER_LOGIN -o SendEnv=REMOTE_USERNAME -o SendEnv="GIT_*" -p $SERVER_PORT "(cd $SERVER_DIR/$serverProjectDir; $COMMAND 2>&1)"