command! UpdateSuggestDB call vim_sql_suggest#UpdateSuggestDB()

inoremap <LocalLeader>sc <C-R>=SQLComplete("column")<CR>
inoremap <LocalLeader>st <C-R>=SQLComplete("table")<CR>
