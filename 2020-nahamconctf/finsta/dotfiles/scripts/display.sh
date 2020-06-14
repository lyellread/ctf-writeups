#!/usr/bin/env bash

rofi_command="rofi -theme themes/i3layoutmenu.rasi"

single_icon=""
dual_icon=""
mirror_icon=""

# Get names of eDP and HDMI displays. We assume only 2 displays, because I never
# have more than 1 external display on my laptop.
BUILTIN_DISPLAY=$(xrandr -q | grep "connected" | grep -v "disconnected" | \
	grep "DP" | cut -d" " -f1 | head -n1)
SECONDARY_DISPLAY=$(xrandr -q | grep "connected" | grep -v "disconnected" | \
	grep "HDMI" | cut -d" " -f1 | head -n1)

# If there is no external display, only show the "single" option, obviously.
if [[ -z "$SECONDARY_DISPLAY" ]]; then
	chosen="$(echo -e "$single_icon" | $rofi_command -dmenu -selected-row 1)"
else
	chosen="$(echo -e "$single_icon\n$dual_icon\n$mirror_icon" | \
		$rofi_command -dmenu -selected-row 1)"
fi

# Perform the selected operation
case $chosen in
	$single_icon)
		xrandr --auto
		[[ -z "$SECONDARY_DISPLAY" ]] || xrandr --output "$SECONDARY_DISPLAY" --off
		xrandr --output "$BUILTIN_DISPLAY" --auto
		;;
	$dual_icon)
		xrandr --output "$BUILTIN_DISPLAY" --auto \
			--output "$SECONDARY_DISPLAY" --right-of "$BUILTIN_DISPLAY" \
			--mode 3840x2160
		;;
	$mirror_icon)
		xrandr --output "$BUILTIN_DISPLAY" --auto \
			--output "$SECONDARY_DISPLAY" --same-as "$BUILTIN_DISPLAY"
		;;
esac
