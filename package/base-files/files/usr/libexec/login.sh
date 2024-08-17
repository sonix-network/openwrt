#!/bin/sh

[ "$(uci -q get system.@system[0].ttylogin)" = 1 ] || exec /bin/ash --login

[ -x /usr/bin/login ] && exec /usr/bin/login

exec /bin/login
