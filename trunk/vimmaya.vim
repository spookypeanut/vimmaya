" Only do this when not done yet for this buffer
if exists("b:loaded_py_maya")
  finish
endif
let b:loaded_py_maya = 1

pyfile ~/.vim/plugin/vimmaya.py

" TODO list
"	allow multi-line ifs, etc via range
"	,MO (select object under cursor)
"	get command port proc to check if one is already open
"	make oo (BIG)
"	command port proc should be able to open any port number
" 	vim should be able to receive on any port number

vmap ,m :python MayaRange()<CR>
nmap ,m :python MayaLine()<CR>
map ,MC :python MayaClear()<CR>
map ,MD :python MayaSubmitIt("help -doc \"\"")<CR>
map ,MH :python MayaSubmitIt("help \"\"")<CR>
map ,MI :python MayaInit()<CR>:python MayaTest()<CR>
map ,MP :python MayaSubmitIt("vimmayaFindProc \"\"")<CR>
map ,MQ :python MayaScratch()<CR>
map ,MS :python MayaSourceCurrent()<CR>
map ,MT :python MayaTest()<CR>

autocmd VimLeavePre * :python MayaQuit()

python MayaInit()
