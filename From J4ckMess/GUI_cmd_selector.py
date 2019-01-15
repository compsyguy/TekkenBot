from tkinter import *
from cmd_name_parser import *
import sys

ordered_list=[]

if len(sys.argv) != 2:
    print("Usage:"+sys.argv[0]+" CharName")
    sys.exit()

def get_name():
    return str(sys.argv[1].capitalize())

char=get_name()

def onselect(evt):
    # Tkinter passes an event object to onselect()
    #ordered_list=[]
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    if value in ordered_list :
        #w.itemconfig(int(index),bd=15)
        ordered_list.remove(value)
        print(ordered_list,'\n')
    else :
        #w.itemconfig(int(index),bd=10)
        ordered_list.append(value)
        print(ordered_list,'\n')
    #print('You selected item %d: "%s"' % (index, value))
    #print(ordered_list)
    # "if déjà in list : pop()"

def main():
    #ordered_list=[]
    cmds=[]
    ls=[]
    character=char
    cmds=commands_name(parse_character(character))

    root = Tk()
    root.title('cmd selector')
    # Configuration du gestionnaire de grille
    #root.rowconfigure(0, weight=1)
    #root.columnconfigure(0, weight=1)
    # Simple button
    selector=Frame(root)
    quitb = Button(selector, text='Exit', command=root.quit)
    # Place button in root

    validateb = Button(selector, text="Validate", command=root.quit)

    listbox= Listbox(selector, selectmode=BROWSE, height=25, bd=15, width=80, font=('Comic Sans MS',14))
    for i in cmds :
        listbox.insert('end',i)
    move_length=Label(root,text="Movelist size ="+str(listbox.size()))

    move_length.pack()
    selector.pack()
    listbox.pack()
    quitb.pack(side=RIGHT,padx=50, pady=25, fill=X)
    validateb.pack(side=LEFT,padx=50, pady=25, fill=X)

    listbox.bind('<<ListboxSelect>>', onselect)


    root.mainloop()
    f=open(character+"_orderedlist.txt",'w')
    for i in ordered_list:
        f.write(i+'\n')
    #print(ordered_list)
main()
