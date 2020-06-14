#!/usr/bin/env zsh

# MPC isn't running
if mpc 2>&1 | grep "Connection refused" > /dev/null; then
	echo ""
	exit 0
fi

STATUS=""
if mpc status | grep "playing" 2>&1 >/dev/null; then
	STATUS=" $(mpc current) $(mpc status | grep "playing" | tr -s ' ' | cut -d' ' -f3)"
else
	STATUS=" $(mpc current)"
fi

echo "$STATUS"
