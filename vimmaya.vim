" Only do this when not done yet for this buffer
if exists("b:loaded_py_maya")
  finish
endif
let b:loaded_py_maya = 1

pyfile ~/.vim/plugin/vimmaya.py

" TODO: 
" 		,MF (find function and split the file)
"		,MC (clear history)
"		,MO (open outliner?)

vmap ,m :python MayaRange()<CR>
nmap ,m :python MayaLine()<CR>
map ,MQ :python MayaScratch()<CR>
map ,MI :python MayaInit()<CR>
map ,MT :python MayaTest()<CR>
map ,MS :python MayaSourceCurrent()<CR>

autocmd VimLeavePre * :python MayaQuit()

python MayaInit()
