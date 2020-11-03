import vim
from vim_sql_suggest import *

def updateCompletionList():
    complete_for = vim.eval("a:completeFor")
    if complete_for == "table":
        vim.command("let b:completionList = {}".format(get_table_names(vim.eval("g:suggest_db"))))
    else:
        vim.command("let b:completionList = {}".format(get_column_names(vim.eval("g:suggest_db"), vim.eval("a:wordToComplete"))))

def updateSuggestDB():
    def python_input(message = 'input'):
        vim.command('call inputsave()')
        vim.command("let user_input = input('" + message + ": ')")
        vim.command('call inputrestore()')
        return vim.eval('user_input')

    current_db = int(vim.eval('exists("g:suggest_db")'))
    print("The current database is: {}".format(vim.eval("g:suggest_db") if current_db else "Undefined"))
    new_db = python_input("Enter the desired DB")
    vim.command('let g:suggest_db = "{}"'.format(new_db))
