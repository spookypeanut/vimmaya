" Only do this when not done yet for this buffer
if exists("b:loaded_py_maya")
  finish
endif
let b:loaded_py_maya = 1

pyfile ~/.vim/plugin/vimmaya.py

vmap ,m :python MayaRange()<CR>
nmap ,m :python MayaLine()<CR>
map ,MS :python MayaScratch()<CR>
map ,MI :python MayaInit()<CR>
map ,MT :python MayaTest()<CR>

autocmd VimLeavePre * :python MayaQuit()

python MayaInit()
