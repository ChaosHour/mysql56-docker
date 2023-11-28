#!/bin/bash
set -e

## ProxySQL entrypoint
## ===================
##
## Supported environment variable:
##
## MONITOR_CONFIG_CHANGE={true|false}
## - Monitor /etc/proxysql.cnf for any changes and reload ProxySQL automatically
## Borrowed from https://github.com/severalnines/proxysql-docker/blob/master/2.3/entrypoint.sh


# If command has arguments, prepend proxysql
if [ "${1:0:1}" == '-' ]; then
	CMDARG="$@"
fi

if [ $MONITOR_CONFIG_CHANGE ]; then

	echo 'Env MONITOR_CONFIG_CHANGE=true'
	CONFIG=/etc/proxysql.cnf
	oldcksum=$(cksum ${CONFIG})

	# Start ProxySQL in the background
	proxysql --reload -f $CMDARG &

	echo "Monitoring $CONFIG for changes.."
	inotifywait -e modify,move,create,delete -m --timefmt '%d/%m/%y %H:%M' --format '%T' ${CONFIG} | \
	while read date time; do
		newcksum=$(cksum ${CONFIG})
		if [ "$newcksum" != "$oldcksum" ]; then
			echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++"
			echo "At ${time} on ${date}, ${CONFIG} update detected."
			echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++"
			oldcksum=$newcksum
			echo "Reloading ProxySQL.."
		        killall -15 proxysql
			proxysql --initial --reload -f $CMDARG
		fi
	done
fi

#Only do this if it does not exist:
if [ ! -d /var/lib/proxysql ]; then
	mkdir -p /var/log/proxysql && touch /var/log/proxysql/proxysql.log && chown -R proxysql:proxysql /var/log/proxysql
fi
#pass in as argument to be able to tail -f the log file: 
#--idle-threads -D /var/lib/proxysql -c /etc/proxysql.cnf &> /var/log/proxysql/proxysql.log

# Start ProxySQL with PID 1
exec proxysql -f $CMDARG




