" ================================
" Plugin Imports
" ================================
python3 import sys
python3 sys.path.append(vim.eval('expand("<sfile>:h")'))
python3 from vim_sql_suggest_intf import *

" ================================
" Plugin Function(s)
" ================================

function! vim_sql_suggest#SQLComplete(completeFor)
    call UpdateWordToComplete()
    let l:cursorPosition = col('.')
    execute "normal! A\<space>"
    call UpdateCompletionList(a:completeFor, b:wordToComplete)
    call UpdateMatches()
    redraw!
    call complete(l:cursorPosition, b:matches)
    return ''
endfunc

"""
" A convenience function that informs the user of the current database and
" allows them to provide a connection to a new database.
"""
function! vim_sql_suggest#UpdateSuggestDB()
    python3 updateSuggestDB()
endfunction

"""
" The complete function is called while in insert mode. We check the
" character that is two chars behind the cursor. If it is ' ' then the
" user hasn't specified a word to complete if there is a non ' ' character
" there then we grab the <cWORD> because we need to know if there is a '.'
" at the end of the word that has been entered.
"""
function! UpdateWordToComplete()
    if getline(".")[col(".")-2] == " "
        let b:wordToComplete = ""
    else
        execute "normal! b"
        let b:wordToComplete = expand('<cWORD>')
    endif
endfunction

"""
" The plugin offers to complete either table or columns names. This function
" delegates to the appropriate python function to populate the completionList
" with the desired contents.
"""
function! UpdateCompletionList(completeFor, wordToComplete)
    python3 updateCompletionList()
endfunction

"""
" If the word to complete ends with a '.' then we make the assumption that
" the dot is preceded with a table name and the user wants all of the
" columns for that table returned as complete options.
"""
function! UpdateMatches()
    if b:wordToComplete[len(b:wordToComplete) - 1] == "."
        let b:matches = b:completionList
    else
        let b:matches = []
        for item in b:completionList
            if(match(item["word"],'^'.b:wordToComplete)==0)
                call add(b:matches,item)
            endif
        endfor
    endif
endfunction
