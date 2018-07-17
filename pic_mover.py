#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import math
from file_operator import *

import Tkinter as tk
import tkFont
from PIL import ImageTk, Image

folder_path = "/Users/Kisecu/Desktop/my_software/result1/华为/3月17"
dest_path = "/Users/Kisecu/Desktop/my_software/bags"

all_img_files, subfolders, all_file_names = find_files(folder_path, ["*.jpg", "*.png", ".bmp"])
print all_file_names
img_iter = 0

#This creates the main window of an application
window = tk.Tk()
window.title("Picture Mover")
window.geometry("1024x720")

## display image
#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
img = Image.open(all_img_files[img_iter])
img = img.resize((250, 250), Image.ANTIALIAS)
tk_img = ImageTk.PhotoImage(img)

#The Label widget is a standard Tkinter widget used to display a text or image on the screen.
panel = tk.Label(window, image = tk_img)

#The Pack geometry manager packs widgets in rows or columns.
panel.grid(row=0,column=0)


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
rows_l2 = 30 # number of rows 
cols_l2 = 1
folders_l2 = []
buttons_l2 = []
button_frame_l2 = None
g_iter_l2 = 0

select_button = None

def get_col_num(num, rows):
    cols = int(math.ceil(float(num) / float(rows)))
    return 1 if cols == 0 else cols

def get_rc_index(num, r_n):
    r = num % r_n 
    c = math.floor(float(num) / float(r_n))
    return int(r), int(c)

def forward_to_next_img():
    global img_iter
    if img_iter >= len(all_img_files) - 1:
        print "You have finished all images"
        return
    img_iter += 1
    img = Image.open(all_img_files[img_iter])
    img = img.resize((250, 250), Image.ANTIALIAS)
    tk_img = ImageTk.PhotoImage(img)
    panel.configure(image = tk_img)
    panel.image = tk_img

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
    global select_button
    global dest_path

    if (select_button != None):
        select_button.configure(highlightbackground = "white")
    btn.configure(highlightbackground = "red")
    select_button = btn
    refresh_l2(os.path.join(dest_path, btn.cget("text")))


def l2_button_callback(btn):
    print btn.cget("text")
    img_file_path = all_img_files[img_iter]
    dest_img_file_path = os.path.join(dest_path, select_button.cget("text"), btn.cget("text"), all_file_names[img_iter])
    dest_img_file_path = dest_img_file_path.replace(" ", "\\ ")
    print dest_img_file_path
    cmd_str = 'mv ' + img_file_path + " " + dest_img_file_path
    print cmd_str
    os.system(cmd_str)
    forward_to_next_img()
    return


def refresh_l1():
    global select_button
    global g_iter_l1
    folders_l1 = [ x for x in os.listdir(dest_path) if os.path.isdir(os.path.join(dest_path, x))]
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
    # set l2 button
    global g_iter_l2
    g_iter_l2 = 0
    folder_l2 = [ x for x in os.listdir(l1_path) if os.path.isdir(os.path.join(l1_path, x))]
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
    print sv.get()
    folder_name = os.path.join(dest_path, sv.get())
    folder_name = folder_name.replace(" ", "\\ ")
    os.system('mkdir ' + folder_name)
    refresh_l1()


def make_l1_entry():
    sv = tk.StringVar()
    l1_entry = tk.Entry(button_frame_l1, width=num_letters)
    r, c = get_rc_index(g_iter_l1, rows_l1)
    l1_entry.grid(row=r, column=c)
    l1_entry.configure(textvariable=sv)
    l1_entry.bind('<Return>', (lambda _: l1_entry_callback(l1_entry)))

def l2_entry_callback(sv):
    print sv.get()
    r_path = os.path.join(dest_path, select_button.cget("text"))
    folder_name = os.path.join(r_path, sv.get())
    folder_name = folder_name.replace(" ", "\\ ")
    os.system('mkdir ' + folder_name)
    refresh_l2(r_path)

def make_l2_entry():
    sv = tk.StringVar()
    l2_entry = tk.Entry(button_frame_l2, width=num_letters)
    r, c = get_rc_index(g_iter_l2, rows_l2)
    l2_entry.grid(row=r, column=c)
    l2_entry.configure(textvariable=sv)
    l2_entry.bind('<Return>', (lambda _: l2_entry_callback(l2_entry)))


def next_button_callback(btn):
    forward_to_next_img()
    return

def create_next_button():
    button = tk.Button(window, text="Next")
    button.grid(row=1, column=0, sticky=tk.N + tk.W + tk.E + tk.S)
    button.configure(command=lambda btn=button: next_button_callback(btn))


refresh_l1()
create_next_button()



#Start the GUI
window.mainloop()

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