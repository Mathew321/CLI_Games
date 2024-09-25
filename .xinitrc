killall picom || picom --config $HOME/.config/picom/picom.conf -b
feh --bg-scale ~/.config/rofi/.current_wallpaper &

exec dwm
