TUNNEL_NAME="my_tunnel"
IP=centos@25.14.135.110
SSH="ssh -o StrictHostKeyChecking=no -i /home/to/your/.ssh/key -p 22222"
SSH_TO_SELF="ssh -o StrictHostKeyChecking=no -i /home/to/your/.ssh/key -p 22222"


kill -15 `screen -ls | grep "${TUNNEL_NAME}" | sed 's/\..*$//g'`

set -x


screen -dmS ${TUNNEL_NAME} $SSH -T -R 65001:0.0.0.0:443 $IP $SSH_TO_SELF -T -L 0.0.0.0:1443:0.0.0.0:65001 $IP
