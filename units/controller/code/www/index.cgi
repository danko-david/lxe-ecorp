#!/bin/bash

source /ecorp/.env

PROV_LOG_DIR=/ecorp/data/controller/provision/logs/

page()
{
cat << EOF
Content-type: text/html

<!doctype html>
<html lang="hu">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐧ECorp Management Web Interface</title>
    <link rel="stylesheet" href="/style.css">
	<script type="text/javascript">window.onReadyHooks = [];</script>
</head>
<body>
    <header>
        <a href="/">🐧ECorp Management Web Interface</a>
    </header>
    
    <nav>
        <a href="/">Doc</a>
		<a href="/?page=config_vars">Configuration variables</a>
		<a href="/?page=infra">Infra</a>
		<a href="/?page=ad_users">AD Users</a>
		<a href="/?page=actions">Actions</a>
    </nav>
    
    <content>
        $1
    </content>

    <footer>
        &copy; LinuxEngineering::ECorp - <a target="_blank" href="https://www.linuxengineering.eu/resources/project/ecorp/">Project main page</a>
    </footer>
	<div id="popupOverlay" class="popup-overlay" onclick="closePopup()">
		<div class="popup-window" onclick="event.stopPropagation()">
			<button class="popup-close" onclick="closePopup()">&times;</button>
			<div id="popupContent"></div>
		</div>
	</div>
	<script src="/script.js"></script>
</body>
</html>
EOF
exit 0
}

ajax()
{
	cat << EOF
Content-type: $1

$2
EOF
exit 0
}

tr()
{
	X=${X:-td}
	echo "<tr>"
	for I in "$@"
	do
		echo "<$X>$I</$X>"
	done
	echo "</tr>"
}

_page_infra()
{
cat << EOF
<h1>Containers of the ECorp infrastructure</h1>
<span>Details of all container attached to bridge "<b>$ECORP_CORE_NETWORK_BRIDGE</b>"</span>
<table>
EOF
	X=th tr "Container Name" "DNS Name" "Extra DNS Names" "IP" "Routes"
	docker ps -q \
	| xargs -n 1 docker inspect --format '{{ .Name }} {{.HostConfig.NetworkMode}}' \
	| sed 's#^/##' \
	| grep "$ECORP_CORE_NETWORK_BRIDGE$" \
	| while read -a m
	do
		docker inspect --format $'{{ .Name }}\t{{ index .Config.Labels "com.docker.compose.service" }}\t{{ index .Config.Labels "dns_names" }} \t{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}} \t{{ index .Config.Labels "network_route" }}' $m \
		| while IFS=$'\t' read -a data
		do
			tr "${data[0]/\//}" "${data[1]}.${DNS_CORE_ZONE_NAME}" "${data[2]}" "${data[3]}" "${data[4]}"
		done
	done
	echo '</table>'
}

_page_config_vars()
{
	cat << EOF
	<h1>List of all primary configuration variables set by .env</h1>
	<table>
EOF

	X=th tr "Variable" "Value"
{
	env -i bash << EOF
	set -a
	source /ecorp/.env
	env | grep -vP '^(_|SHLVL|PWD)='
EOF
} | while IFS='=' read -a kv
	do
		tr "${kv[0]}" "${kv[1]}"
	done
	echo "</table>"
}

exec_addc()
{
	docker exec ecorp-dc-1 "$@"
}

dc_data_extract()
{
	local -n arr=$1
	while IFS=":" read -a ent
	do
		arr[${ent[0]}]=${ent[1]:1}
	done <<< "$2"
}

popup_data()
{
	cat << EOF
	<div>
		<button class="popup-activate">$1</button>
		<div class="popup-data" style="display: none;">$2</div>
	</div>
EOF
}

_page_ad_users()
{
	cat << EOF
	<h1>List of users in AD Domain controller: dc.${DNS_CORE_ZONE_NAME}</h1>
	<span>Users imported from "<b>./settings/ad-users.yml</b>". If you just added new users, re-run ECorp provisioning in <a href="/?page=actions">Actions</a> menu.</span>
	<table>
EOF
	X=th tr "Username" "Full name" "Email" "Role title" "All AD records"

	for user in $(exec_addc samba-tool user list | sort)
	do
		raw_data=$(exec_addc samba-tool user show "$user")
		unset DC_USER || true
		declare -A DC_USER
		dc_data_extract DC_USER "$raw_data"
		tr	"${DC_USER['sAMAccountName']}" "${DC_USER['displayName']}"\
			"${DC_USER['mail']}" "${DC_USER['title']}" \
			"$(popup_data "Show all AD records" "<pre>$raw_data</pre>")"
	done
echo '</table>'
}

_page_actions()
{
cat << EOF
	<h1>Actions</h1>
	<table>
		$(X=th tr "Launch action")
		$(tr "<a href="/?raw=start_provision">Start provision</a>")

	</table>
	<table>
		$(X=th tr "Provision logs")
EOF
	
	for f in $(ls -t $PROV_LOG_DIR)
	do
		tr '<a href="/?page=follow_log&file='$f'">'$f'</a>'
	done

echo '</table>'
}

chk_prov()
{
	[ 0 = $(ps aux | grep ansible-playbook | grep -v grep | wc -l) ]
}

_raw_start_provision()
{
	if ! chk_prov
	then
		last_file=$(ls -t ${PROV_LOG_DIR} | head -1)
		page 'Provision already running, follow here: <a href="/?page=follow_log&file='$last_file'">'$last_file'</a>'
		exit 0
	fi

	sudo /ecorp/units/controller/code/ecorp controller_ansible_provision  > /dev/null &

	rem=10
	while chk_prov && [ $rem '>' 0 ]
	do
		rem=$(expr $rem - 1)
		sleep 1
	done

	last_file=$(ls -t ${PROV_LOG_DIR} | head -1)

	echo "Content-Type: text/plain; charset=UTF-8"
	echo "Location: http://"$HTTP_HOST"/?page=follow_log&file="$last_file
	echo ""
}

_page_follow_log()
{
cat << EOF
	<h1>Provisioning log output</h1>
	<table>
EOF
	file=${_GET['file']}

	X=th tr "Following log output of: "$file
cat << EOF
	<tr>
		<td>
			<pre id="log_output_target"></pre>
			<script type="text/javascript">
				window.onReadyHooks.push(
					()=>streamTo('/?raw=follow_log&file=$file', document.getElementById('log_output_target'))
				)
			</script>
		</td>
	</tr>
	</table>
EOF
}

_raw_follow_log()
{
	echo "Content-Type: text/event-stream"
	echo "Cache-Control: no-cache"
	echo "X-Content-Type-Options: nosniff"
	echo ""

	file=${_GET['file']}
	
	tail -n 9999999 -f ${PROV_LOG_DIR}${file} &
	TPID=$?

	exit_file=${PROV_LOG_DIR}${file}".exit"
	
	while ! [ -e $exit_file ]
	do
		sleep 1
	done
	ex=$(cat $exit_file)
	echo "Provisioning exited: "$ex
	kill $TPID
	exit $ex
}

dbg()
{
	echo
	echo "> $@"
	$@
}

_page_dbg()
{
	echo "<pre>"
	set -a
	source /ecorp/.env
	dbg export
	dbg docker ps
	dbg exec_addc samba-tool user list
	echo "</pre>"
}

#### Main - controller routing
declare -A _GET

if [ ! -z $QUERY_STRING ]
then
	IFS='=&' read -a parm <<< "$QUERY_STRING"
	for ((i=0; i<${#parm[@]}; i+=2))
	do
		_GET[${parm[i]}]=${parm[i+1]}
	done
fi

manage_ent()
{
if [ ! -z "${_GET[$1]}" ]
then
	call_page="_$1_${_GET[$1]}"
	if [ $1 = 'raw' ]
	then
		$call_page
	elif [[ $(type -t $call_page) == function ]]
	then
		$1 "$($call_page)"
	else
		page "$1 ${_GET[$1]} does not exists"
	fi
fi

}

# manage docs
if [ ! -z "${_GET['doc']}" ]
then
	doc=$(readlink -f "/ecorp/${_GET['doc']}")
	# render only docs under /doc/
	if [[ "$doc" =~ ^/ecorp/doc/.* ]]
	then
		page "$(pandoc -t html $doc)"
	else
		page "Documentation $doc not found!"
	fi
fi

# manage entities
manage_ent page
manage_ent ajax
manage_ent raw

# main page
page "$(pandoc -t html /ecorp/README.md)"
