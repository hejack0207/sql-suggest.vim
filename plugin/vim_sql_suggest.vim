command! UpdateSuggestDB call vim_sql_suggest#UpdateSuggestDB()

inoremap <LocalLeader>sc <C-R>=vim_sql_suggest#SQLComplete("column")<CR>
inoremap <LocalLeader>st <C-R>=vim_sql_suggest#SQLComplete("table")<CR>
