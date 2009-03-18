" Only do this when not done yet for this buffer
if exists("b:loaded_vimmaya")
  finish
endif
let b:loaded_vimmaya = 1

pyfile ~/.vim/plugin/vimmaya.py

" TODO list
"	Figure out why increasing the size of the output window gives an error
"	Highlighting for maya output
"	Test that e.g. help, docs fuctions work
"	Get the scratch buffer to auto-save
"	get command port proc to check if one is already open
"	make oo (BIG)
"	command port proc should be able to open any port number
" 	vim should be able to receive on any port number

" ,mm	Submit current line / selected range
vmap ,mm :python MayaRange()<CR>
nmap ,mm :python MayaLine()<CR>
" ,mc	Clear output window
map ,mc :python MayaClear()<CR>
" ,md	Open proc under cursor in Maya documentation
map ,md :python MayaSubmitIt("help -doc \"\"")<CR>
" ,mh	Get help for proc under cursor
map ,mh :python MayaSubmitIt("help \"\"")<CR>
" ,mi	Initialize plugin
map ,mi :python MayaInit()<CR>:python MayaTest()<CR>
" ,mo	Select object under cursor
map ,mo :python MayaSubmitIt("select \"\"")<CR>
" ,mp	Open file containing proc under cursor in a new window
map ,mp :python MayaSubmitIt("vimmayaFindProc \"\"")<CR>
" ,mq	Open the Maya scratch buffer in a window
map ,mq :python MayaScratch()<CR>
" ,mr	Rehash
map ,mr :python MayaSubmitIt("rehash; print \"Rehashed\\n\"")<CR>
" ,ms	Source the current buffer (nb: file must be saved)
map ,ms :python MayaSourceCurrent()<CR>
" ,mt	Test connection to Maya (pops up a window, and prints to output window)
map ,mt :python MayaTest()<CR>

autocmd VimLeavePre * :python MayaQuit()

au BufRead,BufNewFile MayaOutput set filetype=mayaoutput

python MayaInit()
