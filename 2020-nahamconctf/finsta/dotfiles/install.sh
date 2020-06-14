#!/usr/bin/env bash

GREEN=`tput setaf 2`
YELLOW=`tput setaf 3`
MAGENTA=`tput setaf 5`
RST=`tput sgr0`

function info {
	echo "[${GREEN}*${RST}] $@"
}

# We need git. How did we get this script without git!? D:
if ! which git >/dev/null; then
	info "installing ${MAGENTA}git${RST}"
	pacman -S git
fi

# We need yay to install AUR packages
if ! which yay >/dev/null; then
	info "installing ${MAGENTA}yay${RST}"
	git clone https://aur.archlinux.org/yay.git
	cd yay
	makepkg -si
	cd ..
fi

info "installing ${MAGENTA}package dependencies${RST}"
packages=$(tr '\n' ' ' < ./packages.txt)
yay -S $packages

info "installing ${MAGENTA}dunst${RST} configuration"
mkdir -p ~/.config/dunst/
ln -s $HOME/.dotfiles/config/dunst/dunstrc $HOME/.config/dunst/dunstrc

info "installing ${MAGENTA}polybar${RST} configuration"
mkdir -p ~/.config/polybar/
ln -s $HOME/.dotfiles/config/polybar/config $HOME/.config/polybar/config

info "installing ${MAGENTA}rofi${RST} configuration"
ln -s $HOME/.dotfiles/config/rofi $HOME/.config/rofi

info "installing ${MAGENTA}rofi-menus{$RST}"
ln -s $HOME/.dotfiles/config/rofi-menus/config.rasi $HOME/.config/rofi/config.rasi
ln -s $HOME/.dotfiles/config/rofi-menus/scripts $HOME/.config/rofi/scripts
ln -s $HOME/.dotfiles/config/rofi-menus/themes $HOME/.config/rofi/themes
ln -s $HOME/.dotfiles/config/rofi-menus/networkmanager-dmenu $HOME/.config/networkmanager-dmenu

# Setup scripts in ~/.local/bin
for file in $(find $HOME/.config/rofi/scripts/ -name '*.sh'); do
	base=$(basename -- "$file")
	noext="${base%.*}"
	ln -s "$file" "$HOME/.local/bin/$noext"
done

info "installing ${MAGENTA}i3${RST} configuration"
mkdir -p ~/.config/i3
ln -s $HOME/.dotfiles/config/i3/config $HOME/.config/i3/config

info "installing ${MAGENTA}X windows${RST} configuration"
ln -s $HOME/.dotfiles/config/xinitrc $HOME/.xinitrc
ln -s $HOME/.dotfiles/config/Xmodmap $HOME/.Xmodmap
ln -s $HOME/.dotfiles/config/Xresources $HOME/.Xresources

info "installing ${MAGENTA}tmux${RST} configuration"
ln -s $HOME/.dotfiles/config/tmux/oh-my-tmux/.tmux.conf $HOME/.tmux.conf
ln -s "$HOME/.dotfiles/config/tmux/tmux.conf.local" "$HOME/.tmux.conf.local"

info "installing ${MAGENTA}zsh${RST} configuration"
ln -s $HOME/.dotfiles/config/zsh/ohmyzsh $HOME/.oh-my-zsh
ln -s $HOME/.dotfiles/config/zsh/zshrc $HOME/.zshrc
mkdir -p $HOME/.oh-my-zsh/custom/plugins
mkdir -p $HOME/.oh-my-zsh/custom/themes
ln -s $HOME/.dotfiles/config/zsh/zsh-autosuggestions $HOME/.oh-my-zsh/custom/plugins/zsh-autosuggestions
ln -s $HOME/.dotfiles/config/zsh/zsh-syntax-highlighting $HOME/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
ln -s $HOME/.dotfiles/config/zsh/zui $HOME/.oh-my-zsh/custom/plugins/zui
ln -s $HOME/.dotfiles/config/zsh/spaceship-prompt/spaceship.zsh-theme $HOME/.oh-my-zsh/custom/themes/spaceship.zsh-theme

info "installing ${MAGENTA}neovim${RST} configuration"
mkdir -p $HOME/.local/share/nvim/site/autoload
ln -s $HOME/.dotfiles/config/vim-plug/plug.vim $HOME/.local/share/nvim/site/autoload/plug.vim

# There may already be a configuration from the base install
if [ -f "$HOME/.config/nvim/init.vim" ]; then
	rm -f "$HOME/.config/nvim/init.vim"
fi

ln -s $HOME/.dotfiles/config/neovim/init.vim $HOME/.config/nvim/init.vim
nvim +PlugInstall +qall
