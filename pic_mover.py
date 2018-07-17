#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import subprocess
import math
from file_operator import *
sys.path.append("/Users/Kisecu/Desktop/my_software/taobaofier")

import Tkinter as tk
import tkFont
from PIL import ImageTk, Image
import tkFileDialog

folder_path = "/Users/Kisecu/Desktop/my_software/result1/华为/4月23"
dest_path = "/Users/Kisecu/Desktop/my_software/super_store/best_seller"
other_path = "/Users/Kisecu/Desktop/my_software/super_store/other"
recycle_path = "/Users/Kisecu/Desktop/my_software/super_store/recycle"

# folder_path = "./test/src"
# dest_path = "./test/dest/dest"
# other_path = "./test/dest/other"
op = "mv" # cp or mv
num_letters = 12

# level - 1 folder
rows_l1 = 15 # number of rows 
cols_l1 = 1 # number of cols
st_col_l1 = 1 # start column
folders_l1 = []
buttons_l1 = []
button_frame_l1 = None
g_iter_l1 = 0

# level-2 folders
rows_l2 = 20 # number of rows 
cols_l2 = 1
folders_l2 = []
buttons_l2 = []
button_frame_l2 = None
g_iter_l2 = 0

select_button = None
unfinished_count_text = None

reach_end = False

msg = None
default_msg = ":)"
error_msg = ":("
finish_msg = "Finish All"

tk_msg_default = None
tk_msg_err = None
tk_msg_finish = None

window = None

all_img_files = None
subfolders = None 
all_file_names = None

def get_col_num(num, rows):
    cols = int(math.ceil(float(num) / float(rows)))
    return 1 if cols == 0 else cols

def get_rc_index(num, r_n):
    r = num % r_n 
    c = math.floor(float(num) / float(r_n))
    return int(r), int(c)


def show_img():
    tk_img = load_img(all_img_files[img_iter])
    panel.configure(image = tk_img)
    panel.image = tk_img


def load_img(filename):
    img = Image.open(filename)
    img = img.resize((250, 250), Image.ANTIALIAS)
    return ImageTk.PhotoImage(img)


def set_msg(msg_type, msg_str=""):
    global msg_panel
    if msg_type == "default":
        print "set to default"
        msg_panel.configure(image = tk_msg_default)
        msg_panel.image = tk_msg_default
        msg.set(default_msg)
    elif msg_type == "error":
        print "set to error"
        msg_panel.configure(image = tk_msg_err)
        msg_panel.image = tk_msg_err
        msg.set(error_msg)
    elif msg_type == "finish":
        print "set to finish"
        msg_panel.configure(image = tk_msg_finish)
        msg_panel.image = tk_msg_finish
        msg.set(finish_msg)
    else:
        msg.set(msg_type)


def forward_to_next_img():
    global img_iter
    global reach_end
    # global unfinished_count_text
    if reach_end:
        set_msg("finish")
        return
    img_iter += 1
    unfinished_count_text.set(str(len(all_img_files) - img_iter))
    if img_iter >= len(all_img_files):
        set_msg("finish")
        reach_end = True
        return
    show_img()

def do_excution(src_file, dest_file):
    if os.path.isfile(dest_file):
        idx = 1
        filename, file_extension = os.path.splitext(dest_file)
        while (1):
            new_name = filename + "(" + str(idx) + ")" + file_extension
            if not os.path.isfile(new_name):
                dest_file = new_name
                break
        idx += 1
        print "File already exist: rename to " + dest_file
    cmd_str = op + src_file + " " + dest_file
    print cmd_str
    if (subprocess.call([op, src_file, dest_file]) != 0):
        print "Error, cannot operate file"
        return False
    return True

def make_dir(dir_name):
    if subprocess.call(['mkdir', dir_name]):
        print "Cannot Create Folder"
        return False
    return True


def refresh_button_frame_l1(file_num=0):
    global button_frame_l1
    global cols_l1
    if button_frame_l1 is not None:
        button_frame_l1.destroy()
    grid_num = file_num + 1 # plus entry
    col_l1 = get_col_num(grid_num, rows_l1)
    button_frame_l1 = tk.Frame(window)
    button_frame_l1.grid(row=0, column=st_col_l1, rowspan=rows_l1, columnspan=cols_l1, sticky=tk.N)


def refresh_button_frame_l2(file_num=0):
    global button_frame_l2
    if button_frame_l2 is not None:
        button_frame_l2.destroy()
    grid_num = file_num + 1 # plus entry
    col_l2 = get_col_num(grid_num, rows_l2)
    button_frame_l2 = tk.Frame(window)
    button_frame_l2.grid(row=0, column=st_col_l1 + cols_l1, rowspan=rows_l2, columnspan=cols_l2, sticky=tk.N)


def l1_button_callback(btn):
    print "pressed l1 button"
    global select_button
    global dest_path
    set_msg("default")

    if (select_button != None):
        select_button.configure(highlightbackground = "white")
    btn.configure(highlightbackground = "red")
    select_button = btn
    refresh_l2(os.path.join(dest_path, btn.cget("text")))


def l2_button_callback(btn):
    print "pressed l2 button"    
    set_msg("default")
    print btn.cget("text")
    if reach_end:
        set_msg("finish")
        return
    img_file_path = all_img_files[img_iter]
    dest_img_file_path = os.path.join(dest_path, select_button.cget("text"), btn.cget("text"), all_file_names[img_iter])
    dest_img_file_path = dest_img_file_path.replace(" ", "\\ ")
    print dest_img_file_path
    if do_excution(img_file_path, dest_img_file_path):
        forward_to_next_img()
    else:
        set_msg("error")


def refresh_l1():
    print "refresh l1"
    global select_button
    global g_iter_l1
    folders_l1 = [ x for x in os.listdir(dest_path) if os.path.isdir(os.path.join(dest_path, x))]
    folders_l1.sort()
    refresh_button_frame_l1(file_num=len(folders_l1))
    refresh_button_frame_l2(file_num=0) # directly destroy 2 and need reselect
    g_iter_l1 = 0
    for f in folders_l1:
        r, c = get_rc_index(g_iter_l1, rows_l1)
        button = tk.Button(button_frame_l1, text=f, width=num_letters, height=2)
        button.grid(row=r, column=c, sticky=tk.N + tk.W + tk.E + tk.S)
        button.configure(command=lambda btn=button: l1_button_callback(btn))
        g_iter_l1 += 1
    make_l1_entry()
    select_button=None


def refresh_l2(l1_path):
    print "refresh l2"
    # set l2 button
    global g_iter_l2
    g_iter_l2 = 0
    folder_l2 = [ x for x in os.listdir(l1_path) if os.path.isdir(os.path.join(l1_path, x))]
    folder_l2.sort()
    refresh_button_frame_l2(file_num=len(folders_l2))
    buttons_l2 = []
    for f in folder_l2:
        button = tk.Button(button_frame_l2, text=f, width=num_letters, height=1)
        r, c = get_rc_index(g_iter_l2, rows_l2)
        button.grid(row=r, column=c, sticky=tk.N + tk.W + tk.E + tk.S)
        button.configure(command=lambda btn=button: l2_button_callback(btn))
        g_iter_l2 += 1
    make_l2_entry()

def l1_entry_callback(sv):
    print "l1 entry entered"
    set_msg("default")
    print sv.get()
    folder_name = os.path.join(dest_path, sv.get())
    if not make_dir(folder_name):
        set_msg("error")
    refresh_l1()


def make_l1_entry():
    sv = tk.StringVar()
    l1_entry = tk.Entry(button_frame_l1, width=num_letters)
    r, c = get_rc_index(g_iter_l1, rows_l1)
    l1_entry.grid(row=r, column=c)
    l1_entry.configure(textvariable=sv)
    l1_entry.bind('<Return>', (lambda _: l1_entry_callback(l1_entry)))

def l2_entry_callback(sv):
    print "l2 entry entered"
    set_msg("default")
    print sv.get()
    r_path = os.path.join(dest_path, select_button.cget("text"))
    folder_name = os.path.join(r_path, sv.get())
    if not make_dir(folder_name):
        set_msg("error")
    refresh_l2(r_path)

def make_l2_entry():
    sv = tk.StringVar()
    l2_entry = tk.Entry(button_frame_l2, width=num_letters)
    r, c = get_rc_index(g_iter_l2, rows_l2)
    l2_entry.grid(row=r, column=c)
    l2_entry.configure(textvariable=sv)
    l2_entry.bind('<Return>', (lambda _: l2_entry_callback(l2_entry)))


def create_count():
    global unfinished_count_text
    unfinished_count_text = tk.StringVar()
    label = tk.Message(window, textvariable = unfinished_count_text, width=1000)
    unfinished_count_text.set(str(len(all_img_files)))
    label.grid(row=1, column=0, sticky=tk.N + tk.W + tk.E + tk.S)


def create_msg():
    global msg
    msg = tk.StringVar()
    label = tk.Message(window, textvariable = msg, width=1000)
    label.grid(row=2, column=0, sticky=tk.N + tk.W + tk.E + tk.S)


def next_button_callback(btn):
    print "pressed next button"
    set_msg("default")
    forward_to_next_img()
    return

def create_next_button():
    button = tk.Button(window, text="Next")
    button.grid(row=3, column=0, sticky=tk.N + tk.W + tk.E + tk.S)
    button.configure(command=lambda btn=button: next_button_callback(btn))


def move_to_other_button_callback(btn):
    set_msg("default")
    if reach_end:
        set_msg("finish")
        return
    img_file_path = all_img_files[img_iter]
    dest_img_file_path = os.path.join(other_path, all_file_names[img_iter])
    if do_excution(img_file_path, dest_img_file_path):
        forward_to_next_img()
    else:
        set_msg("error")


def create_move_to_other_button():
    button = tk.Button(window, text="Move to Other")
    button.grid(row=4, column=0, sticky=tk.N + tk.W + tk.E + tk.S)
    button.configure(command=lambda btn=button: move_to_other_button_callback(btn))


def recycle_button_callback(btn):
    set_msg("default")
    if reach_end:
        set_msg("finish")
        return
    img_file_path = all_img_files[img_iter]
    dest_img_file_path = os.path.join(recycle_path, all_file_names[img_iter])
    if do_excution(img_file_path, dest_img_file_path):
        forward_to_next_img()
    else:
        set_msg("error")


def create_recycle_button():
    button = tk.Button(window, text="Recycle")
    button.grid(row=5, column=0, sticky=tk.N + tk.W + tk.E + tk.S)
    button.configure(command=lambda btn=button: recycle_button_callback(btn))


def open_folder():
    global folder_path
    folder_path = tkFileDialog.askdirectory()
    print folder_path
    runGUI()

def init_window():
    global window
    window = tk.Tk()
    window.title("Picture Mover")
    window.geometry("1024x720")

    menubar = tk.Menu(window)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=open_folder)
    menubar.add_cascade(label="Folder", menu=filemenu)
    window.config(menu=menubar)
    #Start the GUI
    window.mainloop()

def runGUI():
    global window, all_img_files, subfolders, all_file_names, img_iter, panel, tk_msg_default, tk_msg_err, tk_msg_finish, msg_panel
    all_img_files, subfolders, all_file_names = find_files(folder_path, ["*.jpg", "*.png", ".bmp"])
    print all_file_names
    img_iter = 0


    #This creates the main window of an application

    #The Label widget is a standard Tkinter widget used to display a text or image on the screen.
    panel = tk.Label(window)
    panel.grid(row=0,column=0)
    show_img()

    create_count()
    create_msg()

    tk_msg_default = load_img("./icon/good.jpg")
    tk_msg_err = load_img("./icon/error.jpg")
    tk_msg_finish = load_img("./icon/finish_all.jpg")
    msg_panel = tk.Label(window)
    msg_panel.grid(row=6,column=0)
    set_msg("default")

    refresh_l1()
    create_next_button()
    create_move_to_other_button()
    create_recycle_button()

    window.update()
    #Start the GUI
    # window.mainloop()

init_window()

# def main():


# if __name__ == '__main__':
#     # parser = argparse.ArgumentParser(description='taobaofier')
#     # parser.add_argument('--input', required=True,
#     #                     help='the path to you want to convert')
#     # parser.add_argument('--output', required=True,
#     #                     help='the path to you want to store results')
#     # args = parser.parse_args()
#     # main(folder_path=args.input, output_path=args.output)
#     main()