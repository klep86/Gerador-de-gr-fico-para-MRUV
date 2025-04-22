import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk




S0 = float(input("Escreva a posição inicial: "))
v0 = float(input("Escreva a velocidade inicial: "))
a = float(input("Escreva a aceleração (ela poderá ser mudada na tabela): "))


def plot_graphs():

  valores_a = treeview_mruv.item("I003").get("values")
  valores_v = treeview_mruv.item("I002").get("values")
  valores_s = treeview_mruv.item("I001").get("values")

  valores_a = [float(i) for i in valores_a]
  valores_v = [float(i) for i in valores_v]
  valores_s = [float(i) for i in valores_s]

  if (var_s.get() == 1):
    plt.figure()
    plt.plot(x_l,valores_s, marker='o')
    plt.xticks(np.arange(0, 11))
    plt.xlabel('t(s)')
    plt.ylabel('s(m)')
    plt.axhline(0, color='0')
    plt.grid()
    for i, (xi, yi) in enumerate(zip(x_l, valores_s)):
      plt.annotate(f'{yi}',
                   (xi, yi),
                   xytext=(0, 10),
                   textcoords='offset points',
                   ha='center',
                   va='bottom')


  if (var_v.get() == 1):
    plt.figure()
    plt.plot(x_l, valores_v, marker = 'o')
    plt.xticks(np.arange(0,11))
    plt.yticks(valores_v)
    plt.xlabel('t(s)')
    plt.ylabel('v(m/s)')
    plt.axhline(0, color='0')
    plt.grid()
    for i, (xi, yi) in enumerate(zip(x_l, valores_v)):
      plt.annotate(f'{yi}',
                   (xi, yi),
                   xytext=(0, 10),
                   textcoords='offset points',
                   ha='center',
                   va='bottom')


  if (var_a.get() == 1):
    plt.figure()
    plt.plot(x_l, valores_a, marker = 'o')
    plt.xticks(np.arange(0, 11))
    plt.yticks(valores_a)
    plt.xlabel('t(s)')
    plt.ylabel('a(m/s²)')
    plt.axhline(0, color='0')
    plt.grid()
    for i, (xi, yi) in enumerate(zip(x_l, valores_a)):
      plt.annotate(f'{yi}',
                   (xi, yi),
                   xytext=(0, 10),
                   textcoords='offset points',
                   ha='center',
                   va='bottom')


  plt.show()





x_l = [0,1,2,3,4,5,6,7,8,9,10]
posição = []

velocidade = [v0,0,0,0,0,0,0,0,0,0,0]
aceleração = [a,a,a,a,a,a,a,a,a,a,a]


for t in x_l:
    posição.append(S0 + v0 * t + a/2 * t**2)
    velocidade[x_l.index(t)] = v0 + a * t


class TreeviewEdit(ttk.Treeview):
  def _init__(self, master, **kw):
    super().__init__(master, **kw)



if __name__ == "__main__":
  root = tk.Tk()
  treeview_mruv = TreeviewEdit(root)
  treeview_mruv.pack(expand=True)
  var_s = tk.IntVar()
  var_v = tk.IntVar()
  var_a = tk.IntVar()

  label = tk.Label(root,text="Gráficos").pack(side="left")
  c1 = tk.Checkbutton(root, text="sxt",variable=var_s, onvalue=1, offvalue=0).pack(side="left")
  c2 = tk.Checkbutton(root, text="vxt",variable=var_v, onvalue=1, offvalue=0).pack(side="left")
  c3 = tk.Checkbutton(root, text="axt",variable=var_a, onvalue=1, offvalue=0).pack(side="left")
  button = tk.Button(root, text= "Gerar gráficos", command=plot_graphs).pack()



  def double_click(event):

    column = treeview_mruv.identify_column(event.x)
    column_index = int(column[1:]) - 1
    row = treeview_mruv.identify_row(event.y)


    selected_iid = treeview_mruv.focus()
    selected_values = treeview_mruv.item(selected_iid)
    column_box = treeview_mruv.bbox(selected_iid,column)



    if row == "I003" and column_index > -1:
        selected_values = selected_values.get("values")[column_index]
    else:
      return
    entry_edit = ttk.Entry(root)
    entry_edit.place(x=column_box[0],
                     y=column_box[1],
                     w=column_box[2],
                     h=column_box[3])

    def on_focus_out(event):
      event.widget.destroy()
    entry_edit.bind("<FocusOut>", on_focus_out)

    def on_enter_pressed(event):
      new_text = event.widget.get()
      selected_iid = event.widget.editing_item_iid
      current_values = treeview_mruv.item(selected_iid).get("values")
      current_values[column_index] = new_text
      treeview_mruv.item(selected_iid, values=current_values)
      NT = new_text
      CI = column_index




      posição = treeview_mruv.item("I001").get("values")
      aceleração = treeview_mruv.item("I003").get("values")
      velocidade = treeview_mruv.item("I002").get("values")

      posição = [float(i) for i in posição]
      aceleração = [float(i) for i in aceleração]
      velocidade = [float(i) for i in velocidade]


      for i in range(len(aceleração)):
        if column_index == 0 and i < 10:
          i += 1
        if i >= column_index:
          aceleração[i] =float(NT)
          velocidade[i] = aceleração[i] + velocidade[i-1]
          posição[i] = aceleração[i]/2 + velocidade[i-1] + posição[i-1]
          treeview_mruv.set("I001",column=i, value = float(posição[i]))
          treeview_mruv.set("I003", column=i, value=NT)
          treeview_mruv.set("I002", column=i, value = float(velocidade[i]))



      event.widget.destroy()


    entry_edit.bind("<Return>", on_enter_pressed)

    entry_edit.editing_column_index = column_index
    entry_edit.editing_item_iid = selected_iid
    entry_edit.insert(0,selected_values)
    entry_edit.select_range(0,tk.END)
    entry_edit.focus()


  root.bind('<Double-1>', double_click)

  column_names = x_l
  treeview_mruv.configure(columns=column_names)
  for i in x_l:
    treeview_mruv.heading(i, text=i)
    treeview_mruv.column(i, width=100)
    treeview_mruv.column(i, anchor=tk.CENTER)

treeview_mruv.heading("#0", text="t(s)", anchor=tk.CENTER)
treeview_mruv.column("#0", width=100)
treeview_mruv.column("#0", anchor=tk.CENTER)

treeview_mruv.insert(parent="", index=1, text="s(m)", values=posição)
treeview_mruv.insert(parent="",index=2,text="v(m/s)", values=velocidade)
treeview_mruv.insert(parent="",index=3,text="a(m/s)", values=aceleração)

root.mainloop()










