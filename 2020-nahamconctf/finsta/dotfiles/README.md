# .dotfiles - Arch User Applications Configuration

This repository holds all the configuration for my user applications running on
top of Arch Linux, although the same configuration should work for any
distribution with the same applications installed.

## Requirements

- Python 3.7+
- Pip
	- thefuck
- Ruby
- Perl
	- Data::Dumper
	- AnyEvent::I3
- i3
- X.Org
- neovim
- dunst
- polybar
- rofi
- tmux
- zsh

## Installation

Clone the repository to `$HOME/.dotfiles`:

```
$ git clone --recursive https://github.com/nahamcontron/dotfiles .dotfiles
```

Run the install script:

```
$ cd .dotfiles
$ ./install.sh
```

You can now change your default shell to `zsh` to activate most of the
configurations installed previously. This script will not install any dependant
programs. It only sets up the configuration files in the correct locations.


