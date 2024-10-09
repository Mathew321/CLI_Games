killall picom || picom --config $HOME/.config/picom/picom.conf -b
feh --bg-scale /home/jack/.config/rofi/.current_wallpaper &
slstatus &

dbus-launch --exit-with-session dwm
