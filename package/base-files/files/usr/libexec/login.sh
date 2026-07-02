#!/bin/sh

[ -t 0 ] && {
	tty_dev=$(readlink /proc/self/fd/0)
	case "$tty_dev" in
		/dev/console|/dev/tty[0-9]*)
			export TERM=${TERM:-linux}
			;;
		/dev/*)
			export TERM=vt102
			;;
	esac
}

# Pick an available login binary: busybox provides /bin/login, the shadow suite
# provides /usr/bin/login. Both support "-f <user>" (force login, no password).
login_bin=/bin/login
[ -x "$login_bin" ] || login_bin=/usr/bin/login

[ "$(uci -q get system.@system[0].ttylogin)" = 1 ] || exec "$login_bin" -f root

exec "$login_bin"
