" Only do this when not done yet for this buffer
if exists("b:loaded_py_maya")
  finish
endif
let b:loaded_py_maya = 1

pyfile ~/.vim/plugin/vimmaya.py

" TODO: Figure out why a lot of output isn't coming through
"		,MC (clear history)
"		,MO (open outliner?)
" 		,MF (find function and split the file)
"		,MS (source current file)

vmap ,m :python MayaRange()<CR>
nmap ,m :python MayaLine()<CR>
map ,MQ :python MayaScratch()<CR>
map ,MI :python MayaInit()<CR>
map ,MT :python MayaTest()<CR>
"map ,MS :python MayaSubmitIt("source " + %:p

autocmd VimLeavePre * :python MayaQuit()

python MayaInit()
