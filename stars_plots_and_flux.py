import tkinter as tk
import matplotlib.pyplot as plt
import astropy.io.fits as pyfits
import numpy as np

# функции для кнопок и возвращения значений
   
def get_file_name():  # открытие файла, получение матрицы
    global file_name
    global scidata
    global xy_btn
    global hdulist
    file_name = file_name_entry.get()
    hdulist = pyfits.open(f"{file_name}")
    scidata = hdulist[0].data
    xy_btn.config(state=tk.NORMAL) # разблокировка следующей кнопки
    #print('1я кнопка')
    #hdulist.close()
    
def get_x_and_y():
    global x_and_y
    global which_plots_btn
    global star_r_btn
    global big_r_btn
    global X
    global Y
    x_and_y = x_entry.get(), y_entry.get()
    X = int(x_and_y[0])
    Y = int(x_and_y[1])
    which_plots_btn.config(state=tk.NORMAL)
    big_r_btn.config(state=tk.NORMAL)

def get_chk_btn():
    global check
    check = plotx_value.get(), ploty_value.get(), plot3D_value.get()
    lets_plot_some_graphs(check)
    print(check)
      
def lets_plot_some_graphs(tup):
    global x_and_y
    global X
    global Y
    if tup[0] == True:
        hor_plot(X - 10, X + 11, Y)
    if tup[1] == True:
        ver_plot(Y - 10, Y + 11, X)
    if tup[2] == True:
        plot_3d(X, Y)
 
def get_stars_r_and_big_r():
    global stars_r
    global big_r
    global big_stars_r
    global X
    global Y
    stars_r = int(star_r_entry.get())
    big_r = int(big_r_entry.get())
    big_stars_r = int(big_stars_r_entry.get())
    flux(X, Y)
    


def hor_plot(x1, x2, y):  # функция для построения горизонтального профиля
    light_hor = scidata[y, x1 - 1:x2 - 1]  # это откладывать по y
    pixels_hor = [_ for _ in range(x1, x2)]  # это по x
    
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)

    ax1.set_title('Горизонтальный профиль звезды')
    ax1.set_xlabel('пиксели, x')
    ax1.set_ylabel('количество фотонов')
    ax1.set_xlim([x1 - 1, x2])
    #ax1.set_ylim([0, maxx])
    ax1.set_xticks([_ for _ in range(x1, x2, 2)] )
    plt.scatter(pixels_hor, light_hor, color = 'black', s=10, marker='*')
    plt.show()
    #print('график1 построился')
    
def ver_plot(y1, y2, x):  # функция для построения вертикального профиля
    light_ver = scidata[y1 - 1:y2 - 1, x]  # по y
    pixels_ver = [_ for _ in range(y1, y2)]  # по x

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)

    ax2.set_title('Вертикальный профиль звезды')
    ax2.set_xlabel('пиксели, y')
    ax2.set_ylabel('количество фотонов')
    ax2.set_xlim([y1 - 1, y2])
    #ax2.set_ylim([0, maxx])
    ax2.set_xticks([_ for _ in range(y1, y2, 2)] )
    plt.scatter(pixels_ver, light_ver, color = 'black', s=10, marker='*')
    plt.show()
    #print('график2 построился')

def plot_3d(x, y):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    x_list = [_ for _ in range(x - 11, x + 10)]
    y_list = [_ for _ in range(y - 11, y + 10)]
    z = scidata[y - 11:y + 10, x - 11:x + 10]
    x_greed, y_greed = np.meshgrid(x_list, y_list)

    ax.plot_surface(x_greed, y_greed, z)
    plt.show()
 
def flux(x, y):
    
    aver_sum = 0
    stars_sum = 0
    big_stars_sum = 0
    for i in range(x - big_r, x + big_r + 1):  # всего фотонов в большом квадрате
        for j in range(y - big_r, y + big_r + 1):
            aver_sum += scidata[j, i]

    for i in range(x - stars_r, x + stars_r + 1):  # фотонов в маленьком квадрате
        for j in range(y - stars_r, y + stars_r + 1):
            stars_sum += scidata[j, i]
            
    for i in range(x - big_stars_r, x + big_stars_r + 1):  # фотонов в среднем квадрате
        for j in range(y - big_stars_r, y + big_stars_r + 1):
            big_stars_sum += scidata[j, i]

    ring_value = aver_sum - big_stars_sum   # количество фотонов в кольце
    ring_space = (2*big_r + 1) ** 2 - (2*big_stars_r + 1)**2  # площадь кольца
    density = ring_value / ring_space
    noise = density * (2*stars_r + 1)**2
    
    exp = hdulist[0].header['exptime']  # время экспозиции
    flux = round((stars_sum - noise) / exp)
                           
    flux_label = tk.Label(win,
                          text=f'{flux}',
                          bg='Plum',
                          fg='DarkSlateBlue')
    flux_label.grid(row=8, column=5, stick='wnes')
 
""" начало оформления окна """   

win = tk.Tk()
win.geometry('800x700')
win.config(bg='RosyBrown')

welcome_label = tk.Label(win,
                         text='Welcome',
                         bg='Plum',
                         fg='DarkSlateBlue'
                         )

welcome_label.grid(row=0, column=0)

file_name_label = tk.Label(win,
                           text='Введите имя файла:',
                           bg='LightSeaGreen',
                           fg='MidnightBlue',
                           padx=31
                           )
file_name_label.grid(row=0, column=1, columnspan=2, stick='w')

file_name_entry = tk.Entry(win, bg='HotPink')
file_name_entry.insert(tk.INSERT, 'v523cas60s-001.fit')
file_name_entry.grid(row=0, column=3, stick='w')

coordinates_label = tk.Label(win,
                             text='Введите координаты объекта:',
                             bg='LightSeaGreen',
                             fg='MidnightBlue'
                             )
coordinates_label.grid(row=1, column=1, columnspan=2, stick='w')

x_label = tk.Label(win,
                   text='x = ',
                   bg='Aqua',
                   fg='MidnightBlue'                   
                   )
y_label = tk.Label(win,
                   text='y = ',
                   bg='Aqua',
                   fg='MidnightBlue'                   
                   )
x_label.grid(row=2, column=1, stick='w')
y_label.grid(row=3, column=1, stick='w')

x_entry = tk.Entry(win)
x_entry.insert(tk.INSERT, '670')
y_entry = tk.Entry(win)
y_entry.insert(tk.INSERT, '1656')
x_entry.grid(row=2, column=2, stick='w')
y_entry.grid(row=3, column=2, stick='w')

file_name_btn = tk.Button(win,
                          text='Ok',
                          command=get_file_name,
                          bg='SeaGreen',
                          fg='Gold'
                          )
file_name_btn.grid(row=0, column=4)

xy_btn = tk.Button(win,
                   text='Ok',
                   command=get_x_and_y,
                   bg='SeaGreen',
                   fg='Gold',
                   state=tk.DISABLED
                   )
xy_btn.grid(row=2, column=3, rowspan=2, stick='w')

plotx_value = tk.IntVar()
plotx_value.set(0)
ploty_value = tk.IntVar()
ploty_value.set(0)
plot3D_value = tk.IntVar()
plot3D_value.set(0)
plotx_chck_btn = tk.Checkbutton(win,
                                text='горизонтальный профиль',
                                bg='LightSalmon',
                                width=23,
                                anchor='w',
                                var=plotx_value,
                                onvalue=1,
                                offvalue=0
                                )
ploty_chck_btn = tk.Checkbutton(win,
                                text='вертикальный профиль',
                                bg='LightSalmon',
                                width=23,
                                anchor='w',
                                var=ploty_value,
                                onvalue=1,
                                offvalue=0
                                )
plot3D_chck_btn = tk.Checkbutton(win,
                                text='3D график',
                                bg='LightSalmon',
                                width=23,
                                anchor='w',
                                var=plot3D_value,
                                onvalue=1,
                                offvalue=0
                                )

plotx_chck_btn.grid(row=4, column=1, columnspan=2, stick='w')
ploty_chck_btn.grid(row=5, column=1, columnspan=2, stick='w')
plot3D_chck_btn.grid(row=6, column=1, columnspan=2, stick='w')

which_plots_btn = tk.Button(win,
                        text='Ok',
                        command=get_chk_btn,
                        bg='SeaGreen',
                        fg='Gold',
                        state=tk.DISABLED
                        )
which_plots_btn.grid(row=4, column=3, rowspan=3, stick='w')

star_r = tk.Label(win,
                  text='введите радиус звезды:',
                  bg='Salmon'
                  )
big_r_lbl = tk.Label(win,
                 text='введите внешний радиус:',
                 bg='Salmon'
                 )
big_stars_r_lbl = tk.Label(win,
                 text='введите внешний радиус звезды:',
                 bg='Salmon'
                 )
star_r.grid(row=0, column=5, stick='w')
big_r_lbl.grid(row=2, column=5, stick='w')
big_stars_r_lbl.grid(row=4, column=5, stick='nw')

big_stars_r_entry = tk.Entry(win, bg='Plum', )
big_stars_r_entry.insert(tk.INSERT, '6')

star_r_entry = tk.Entry(win,
                        bg='Plum')
star_r_entry.insert(tk.INSERT, '4')
big_r_entry = tk.Entry(win,
                       bg='Plum')
big_r_entry.insert(tk.INSERT, '25')
star_r_entry.grid(row=1, column=5, stick='nw')
big_r_entry.grid(row=3, column=5, stick='nw')
big_stars_r_entry.grid(row=5, column=5, stick='nw')


big_r_btn = tk.Button(win,
                       text='Ok',
                       command=get_stars_r_and_big_r,
                       bg='SeaGreen',
                       fg='Gold',
                       state=tk.DISABLED
                       )
big_r_btn.grid(row=6, column=5, stick='new')


win.mainloop()
