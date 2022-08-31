import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import codecs

'''
author: Aamir Shaikh
'''

# Importing difflib
import difflib

root = tk.Tk()
root.title("Compare changes")



def show_differences():
    try:
        first_file = filedialog.askopenfilename()
        second_file = filedialog.askopenfilename()
        #print(first_file, second_file)
        
        with codecs.open(first_file,encoding="utf8", errors='ignore') as file_1:
            file_1_text = file_1.readlines()

        with codecs.open(second_file,encoding="utf8", errors='ignore') as file_2:
                file_2_text = file_2.readlines()

        # Find and print the diff:
        contents = []

        #for line in difflib.context_diff
        row = 0
        col = 0

        
        diff_lines = []
        removed_lines = []
        added_lines = []
        num_lines_added = 0
        num_lines_removed = 0
        
        for cnt, line in enumerate(difflib.unified_diff(
                        file_1_text, file_2_text, fromfile=first_file,
                        tofile=second_file, lineterm='')):               
                if line.strip().startswith('@'):
                    line = '#' * 30 + ' ' + line  + ' ' + '#' * 30
                    #line = '\n ' + line  + '\n '
                    row = str(cnt + 1) + '.0'
                    col = str(cnt + 1) + '.' + str(len(line))
                    cnt += 1
                    diff_lines.append((row,col))
                    
                if line.startswith('-'):
                    row = str(cnt + 1) + '.0'
                    col = str(cnt + 1) + '.' + str(len(line))
                    cnt += 1
                    if not(line.startswith('---')): num_lines_removed  += 1
                    removed_lines.append((row,col))

                if line.startswith('+'):
                    #print(line)
                    row = str(cnt + 1) + '.0'
                    col = str(cnt + 1) + '.' + str(len(line))
                    cnt += 1
                    if not(line.startswith('+++')):num_lines_added += 1
                    added_lines.append((row,col))
                contents.append(line)
                                        
                    
        contents = '\n'.join(contents)
        contents = contents.replace('\n\n','\n')
        output.config(state=tk.NORMAL)
        output.insert('1.0', contents)
        output.config(state=tk.DISABLED)

        for r,c in added_lines:
            output.tag_add("added", r, c)
            output.tag_config("added", background="light green", foreground="black")

        for r,c in removed_lines:
            output.tag_add("removed", r, c)
            output.tag_config("removed", background="pink", foreground="black")


        for r,c in diff_lines:
            output.tag_add("diff", r, c)
            output.tag_config("diff", background="yellow", foreground="black")

        result = f'No. of lines added: {num_lines_added}\nNo. of lines removed: {num_lines_removed}'
        Result.config(text=result)
        output.pack(fill=tk.BOTH, expand=True)
        
    except Exception as e:
        messagebox.showinfo('Error',e)




show_file_diff = tk.Button(root, text="Compare Files", command=show_differences)
show_file_diff.pack()

output = ScrolledText(root)

def clear_screen():
    output.config(state=tk.NORMAL)
    output.delete('1.0', tk.END)
    


clear_diff = tk.Button(root, text="Clear Contents", command=clear_screen)
clear_diff.pack()

Result = tk.Label(root, text="")
Result.pack(side=tk.BOTTOM)


root.mainloop()
