" Setup plugins for vim-plug
call plug#begin('~/.config/nvim/plugged')

Plug 'crusoexia/vim-monokai'
Plug 'tpope/vim-surround'
Plug 'scrooloose/nerdtree'
Plug 'w0rp/ale'
Plug 'airblade/vim-gitgutter'
Plug 'Xuyuanp/nerdtree-git-plugin'
Plug 'vim-airline/vim-airline'
Plug 'hiphish/jinja.vim'
Plug 'psf/black'
Plug 'ncm2/ncm2'
Plug 'ncm2/ncm2-jedi'
Plug 'ncm2/ncm2-bufword'
Plug 'ncm2/ncm2-path'
Plug 'roxma/nvim-yarp'
Plug 'fatih/vim-go', { 'do': ':GoUpdateBinaries' }
Plug 'rust-lang/rust.vim'

call plug#end()

syntax on
silent! colorscheme monokai
set termguicolors
set mouse=a
set autoindent
set tabstop=4
set shiftwidth=4
set softtabstop=4
set number

" Display a visual marker for 80 chars, but don't word-wrap
set textwidth=80
set colorcolumn=+1
set fo-=t

"""
""" NERDTree Settings
"""

" Ctrl-O to open/close nerd tree
map <C-o> :NERDTreeToggle<CR>

" Close VIM if only NERDTree is open
autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTree") && b:NERDTree.isTabTree()) | q | endif

" Start NERDTree if opening a directory
autocmd StdinReadPre * let s:std_in=1
autocmd VimEnter * if argc() == 1 && isdirectory(argv()[0]) && !exists("s:std_in") | exe 'NERDTree' argv()[0] | wincmd p | ene | exe 'cd '.argv()[0] | endif

" Start NERDTree if no file is specified
autocmd StdinReadPre * let s:std_in=1
autocmd VimEnter * if argc() == 0 && !exists("s:std_in") | NERDTree | endif

"""
""" Automatic Linting Engine (ALE) Settings
"""

" Display erros in airline
let g:airline#extensions#ale#enabled = 1

""" I dont understand this, but it makes colors work
""" https://github.com/vim/vim/issues/993#issuecomment-255651605
let &t_8f = "\<Esc>[38;2;%lu;%lu;%lum"
let &t_8b = "\<Esc>[48;2;%lu;%lu;%lum"

"""
""" VIM-Markdown settings
"""

let g:markdown_fenced_languages = ["c", "cpp", "python"]


"""
""" Python-Black Settings
"""

autocmd BufWritePre *.py execute ':Black'

"""
""" Golang settings
"""

"""
""" Rust settings
"""

" Auto-format rust files on save
let g:rustfmt_autosave = 1

"""
""" HTML settings
"""

autocmd FileType html setlocal shiftwidth=2 tabstop=2

"""
""" YAML Settings
"""

autocmd FileType yaml setlocal shiftwidth=2 tabstop=2

"""
""" ncm2 Settings
"""

autocmd BufEnter * call ncm2#enable_for_buffer()
set completeopt=menuone,noselect,noinsert
set shortmess+=c

let ncm2#popup_delay = 5
let ncm2#complete_length = [[1, 1]]
let g:ncm2#matcher = 'substrfuzzy'

" Use <Tab> to accept the autocompletion
inoremap <expr> <Tab> pumvisible() ? "\<C-n>" : "\<Tab>"
inoremap <expr> <S-Tab> pumvisible() ? "\<C-p>" : "\<S-Tab>"

"""
""" Cursor Settings
"""

set guicursor=n-v-c:block,i-ci-ve:ver25,r-cr:hor20,o:hor50,a:blinkwait700-blinkoff400-blinkon250-Cursor/lCursor,sm:block-blinkwait175-blinkoff150-blinkon175

"""
""" Disable middle mouse click
"""

map <MiddleMouse> <LeftMouse>
imap <MiddleMouse> <LeftMouse>

map <2-MiddleMouse> <Nop>
imap <2-MiddleMouse> <Nop>
map <3-MiddleMouse> <Nop>
imap <3-MiddleMouse> <Nop>
map <4-MiddleMouse> <Nop>
imap <4-MiddleMouse> <Nop>
