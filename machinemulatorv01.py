#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
#       29/11/23
# python3
# necesita intelhex -> pip install intelhex

import sys
import tkinter as tk
import tkinter.ttk as ttk       # tk y ttk de widgets
from tkinter.constants import *
import os.path
from threading import Timer     #importo el timer para hacer el clock
from intelhex import IntelHex   #libreria para importar los hex de intel
from tkinter import filedialog as fd    #importo filedialog



_script = sys.argv[0]
_location = os.path.dirname(_script)

#import machinemulatorv01_support

_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
_fgcolor = '#000000'  # X11 color: 'black'
_compcolor = 'gray40' # X11 color: #666666
_ana1color = '#c3c3c3' # Closest X11 color: 'gray76'
_ana2color = 'beige' # X11 color: #f5f5dc
_tabfg1 = 'black' 
_tabfg2 = 'black' 
_tabbg1 = 'grey75' 
_tabbg2 = 'grey89' 
_bgmode = 'light' 
_bg_verde_on = '#a5ffa5' #verde on
_bg_rojo_on  = '#ffa5a5' #rojo on
_bg_amarillo = '#FFFF00' ## amarillo del clock


_style_code_ran = 0
corriendo=0;
clock=0
mem_a = 0
mem_d = 0
ff_q = 0

address=0       # direccion de la FSM
data=0          # dato a representar en la FSM
next_address=0  # proxima direccion
next_data=0     # proxima data (Q del FF)

memoria=[0x55,0xAA,0x40, 0xE9, 0x37, 0x31, 0x56, 0x52, 0x39, 0x00, 0x00, 0x77, 0xCC, 0x56, 0x49] #arreglo que contendra la memoria
intelhex=IntelHex()     # creo un objeto vacio

def _style_code():
    global _style_code_ran
    if _style_code_ran:
       return
    style = ttk.Style()
    if sys.platform == "win32":
       style.theme_use('winnative')
    style.configure('.',background=_bgcolor)
    style.configure('.',foreground=_fgcolor)
    style.configure('.',font='TkDefaultFont')
    style.map('.',background =
       [('selected', _compcolor), ('active',_ana2color)])
    if _bgmode == 'dark':
       style.map('.',foreground =
         [('selected', 'white'), ('active','white')])
    else:
       style.map('.',foreground =
         [('selected', 'black'), ('active','black')])
    style.map('TCheckbutton',background =
           [('selected', _bgcolor), ('active', _ana2color)], indicatorcolor =
           [('selected', _fgcolor), ('!active', _bgcolor)])
    
    style.configure("LedAmOn.TFrame", background=_bg_amarillo)  #configuro estilo del led amarillo on
    style.configure("LedAmOff.TFrame", background=_bgcolor)     #configuro led amarillo off
    style.configure("DataGHigh.TLabel", background=_bg_verde_on)  #configuro estilo del led amarillo on
    style.configure("DataGLow.TLabel", background=_bgcolor)     #configuro led amarillo off
    style.configure("DataRHigh.TLabel", background=_bg_rojo_on)  #configuro estilo del led amarillo on
    style.configure("DataRLow.TLabel", background=_bgcolor)     #configuro led amarillo off
    _style_code_ran = 1

class machinemulator:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        width=570
        height=545
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        top.geometry(alignstr)

        #top.geometry("570x545+813+391")
        top.minsize(1, 1)
        top.maxsize(2145, 1410)
        top.resizable(0,  0)                    # no rezisable
        top.title("FSMachinemulator V0.1")
        top.configure(highlightcolor="black")

        self.top = top
        self.sw_var_a7 = tk.IntVar()
        self.sw_var_a6 = tk.IntVar()
        self.sw_var_a5 = tk.IntVar()
        self.sw_var_a4 = tk.IntVar()

        _style_code()
        self.Memory_tlf = ttk.Labelframe(self.top)
        self.Memory_tlf.place(relx=0.281, rely=0.128, relheight=0.539, relwidth=0.23)
        self.Memory_tlf.configure(relief='')
        self.Memory_tlf.configure(labelanchor="n")
        self.Memory_tlf.configure(text='''Memoria''')
        self.mem_d4 = tk.Label(self.Memory_tlf)
        self.mem_d4.place(relx=0.756, rely=0.34, height=23, width=30, bordermode='ignore')
        self.mem_d4.configure(activebackground="#f9f9f9")
        self.mem_d4.configure(anchor='w')
        self.mem_d4.configure(compound='left')
        self.mem_d4.configure(text='''D4''')
        self.mem_d5 = tk.Label(self.Memory_tlf)
        self.mem_d5.place(relx=0.763, rely=0.272, height=23, width=29, bordermode='ignore')
        self.mem_d5.configure(activebackground="#f9f9f9")
        self.mem_d5.configure(anchor='w')
        self.mem_d5.configure(compound='left')
        self.mem_d5.configure(text='''D5''')
        self.mem_d6 = tk.Label(self.Memory_tlf)
        self.mem_d6.place(relx=0.763, rely=0.204, height=23, width=29, bordermode='ignore')
        self.mem_d6.configure(activebackground="#f9f9f9")
        self.mem_d6.configure(anchor='w')
        self.mem_d6.configure(compound='left')
        self.mem_d6.configure(text='''D6''')
        self.mem_d7 = tk.Label(self.Memory_tlf)
        self.mem_d7.place(relx=0.771, rely=0.136, height=23, width=25, bordermode='ignore')
        self.mem_d7.configure(activebackground="#f9f9f9")
        self.mem_d7.configure(anchor='w')
        self.mem_d7.configure(compound='left')
        self.mem_d7.configure(text='''D7''')
        self.mem_a7 = ttk.Label(self.Memory_tlf)
        self.mem_a7.place(relx=0.084, rely=0.136, height=21, width=28, bordermode='ignore')
        self.mem_a7.configure(background="#d9d9d9")
        self.mem_a7.configure(foreground="#000000")
        self.mem_a7.configure(font="TkDefaultFont")
        self.mem_a7.configure(relief="flat")
        self.mem_a7.configure(anchor='w')
        self.mem_a7.configure(justify='left')
        self.mem_a7.configure(text='''A7''')
        self.mem_a7.configure(compound='left')
        self.mem_a6 = tk.Label(self.Memory_tlf)
        self.mem_a6.place(relx=0.084, rely=0.204, height=23, width=29, bordermode='ignore')
        self.mem_a6.configure(activebackground="#f9f9f9")
        self.mem_a6.configure(anchor='w')
        self.mem_a6.configure(compound='left')
        self.mem_a6.configure(text='''A6''')
        self.mem_a5 = tk.Label(self.Memory_tlf)
        self.mem_a5.place(relx=0.099, rely=0.272, height=23, width=29, bordermode='ignore')
        self.mem_a5.configure(activebackground="#f9f9f9")
        self.mem_a5.configure(anchor='w')
        self.mem_a5.configure(compound='left')
        self.mem_a5.configure(text='''A5''')
        self.mem_a3 = tk.Label(self.Memory_tlf)
        self.mem_a3.place(relx=0.084, rely=0.51, height=23, width=39, bordermode='ignore')
        self.mem_a3.configure(activebackground="#f9f9f9")
        self.mem_a3.configure(anchor='w')
        self.mem_a3.configure(compound='left')
        self.mem_a3.configure(text='''A3''')
        self.mem_a2 = tk.Label(self.Memory_tlf)
        self.mem_a2.place(relx=0.084, rely=0.578, height=23, width=39, bordermode='ignore')
        self.mem_a2.configure(activebackground="#f9f9f9")
        self.mem_a2.configure(anchor='w')
        self.mem_a2.configure(compound='left')
        self.mem_a2.configure(text='''A2''')
        self.mem_a1 = tk.Label(self.Memory_tlf)
        self.mem_a1.place(relx=0.084, rely=0.646, height=23, width=39, bordermode='ignore')
        self.mem_a1.configure(activebackground="#f9f9f9")
        self.mem_a1.configure(anchor='w')
        self.mem_a1.configure(compound='left')
        self.mem_a1.configure(text='''A1''')
        self.mem_a0 = tk.Label(self.Memory_tlf)
        self.mem_a0.place(relx=0.084, rely=0.714, height=23, width=39, bordermode='ignore')
        self.mem_a0.configure(activebackground="#f9f9f9")
        self.mem_a0.configure(anchor='w')
        self.mem_a0.configure(compound='left')
        self.mem_a0.configure(text='''A0''')
        self.mem_d3 = tk.Label(self.Memory_tlf)
        self.mem_d3.place(relx=0.756, rely=0.51, height=23, width=29, bordermode='ignore')
        self.mem_d3.configure(activebackground="#f9f9f9")
        self.mem_d3.configure(anchor='w')
        self.mem_d3.configure(compound='left')
        self.mem_d3.configure(text='''D3''')
        self.mem_d2 = tk.Label(self.Memory_tlf)
        self.mem_d2.place(relx=0.756, rely=0.578, height=23, width=29, bordermode='ignore')
        self.mem_d2.configure(activebackground="#f9f9f9")
        self.mem_d2.configure(anchor='w')
        self.mem_d2.configure(compound='left')
        self.mem_d2.configure(text='''D2''')
        self.mem_d0 = tk.Label(self.Memory_tlf)
        self.mem_d0.place(relx=0.756, rely=0.714, height=23, width=29, bordermode='ignore')
        self.mem_d0.configure(activebackground="#f9f9f9")
        self.mem_d0.configure(anchor='w')
        self.mem_d0.configure(compound='left')
        self.mem_d0.configure(text='''D0''')
        self.mem_d1 = tk.Label(self.Memory_tlf)
        self.mem_d1.place(relx=0.763, rely=0.646, height=23, width=29, bordermode='ignore')
        self.mem_d1.configure(activebackground="#f9f9f9")
        self.mem_d1.configure(anchor='w')
        self.mem_d1.configure(compound='left')
        self.mem_d1.configure(text='''D1''')
        self.mem_label = tk.Label(self.Memory_tlf)
        self.mem_label.place(relx=0.305, rely=0.878, height=23, width=61, bordermode='ignore')
        self.mem_label.configure(activebackground="#f9f9f9")
        self.mem_label.configure(anchor='w')
        self.mem_label.configure(compound='left')
        self.mem_label.configure(text='''256 x 8''')
        self.mem_a4 = tk.Label(self.Memory_tlf)
        self.mem_a4.place(relx=0.084, rely=0.34, height=23, width=29, bordermode='ignore')
        self.mem_a4.configure(activebackground="#f9f9f9")
        self.mem_a4.configure(anchor='w')
        self.mem_a4.configure(compound='left')
        self.mem_a4.configure(text='''A4''')
        self.Clock_tlf = ttk.Labelframe(self.top)
        self.Clock_tlf.place(relx=0.282, rely=0.695, relheight=0.119, relwidth=0.449)
        self.Clock_tlf.configure(relief='')
        self.Clock_tlf.configure(text='''Clock''')
        self.reset_button = ttk.Button(self.Clock_tlf)
        self.reset_button.place(relx=0.43, rely=0.308, height=30, width=83, bordermode='ignore')
        self.reset_button.configure(takefocus="")
        self.reset_button.configure(text='''Reset''')
        self.reset_button.configure(compound='left')
        self.run_stop_button = ttk.Button(self.Clock_tlf)
        self.run_stop_button.place(relx=0.043, rely=0.308, height=30, width=73, bordermode='ignore')
        self.run_stop_button.configure(takefocus="")
        self.run_stop_button.configure(text='''Run''')
        self.run_stop_button.configure(compound='left')
        self.clock_led = ttk.Frame(self.Clock_tlf)
        self.clock_led.place(relx=0.844, rely=0.415, relheight=0.262, relwidth=0.078, bordermode='ignore')
        self.clock_led.configure(relief='groove')
        self.clock_led.configure(borderwidth="2")
        self.clock_led.configure(relief="groove")
        self.SW_tlf = ttk.Labelframe(self.top)
        self.SW_tlf.place(relx=0.111, rely=0.165, relheight=0.211, relwidth=0.128)
        self.SW_tlf.configure(relief='')
        self.SW_tlf.configure(text='''SW IN''')
        self.sw_a7 = ttk.Checkbutton(self.SW_tlf, onvalue=1, offvalue=0, command=click_sw_a7)
        self.sw_a7.place(relx=0.178, rely=0.148, relwidth=0.575, relheight=0.0, height=23, bordermode='ignore')
        self.sw_a7.configure(variable=self.sw_var_a7)
        self.sw_a7.configure(takefocus="")
        self.sw_a7.configure(text='''A7''')
        self.sw_a7.configure(compound='left')
        self.sw_a6 = ttk.Checkbutton(self.SW_tlf, onvalue=1, offvalue=0, command=click_sw_a6)
        self.sw_a6.place(relx=0.178, rely=0.339, relwidth=0.644, relheight=0.0, height=23, bordermode='ignore')
        self.sw_a6.configure(variable=self.sw_var_a6)
        self.sw_a6.configure(takefocus="")
        self.sw_a6.configure(text='''A6''')
        self.sw_a6.configure(compound='left')
        self.sw_a5 = ttk.Checkbutton(self.SW_tlf, onvalue=1, offvalue=0, command=click_sw_a5)
        self.sw_a5.place(relx=0.178, rely=0.504, relwidth=0.575, relheight=0.0, height=33, bordermode='ignore')
        self.sw_a5.configure(variable=self.sw_var_a5)
        self.sw_a5.configure(takefocus="")
        self.sw_a5.configure(text='''A5''')
        self.sw_a5.configure(compound='left')
        self.sw_a4 = ttk.Checkbutton(self.SW_tlf, onvalue=1, offvalue=0, command=click_sw_a4)
        self.sw_a4.place(relx=0.178, rely=0.739, relwidth=0.575, relheight=0.0, height=23, bordermode='ignore')
        self.sw_a4.configure(variable=self.sw_var_a4)
        self.sw_a4.configure(takefocus="")
        self.sw_a4.configure(text='''A4''')
        self.sw_a4.configure(compound='left')
        self.FF_tlf = ttk.Labelframe(self.top)
        self.FF_tlf.place(relx=0.544, rely=0.128, relheight=0.539, relwidth=0.193)
        self.FF_tlf.configure(relief='')
        self.FF_tlf.configure(labelanchor="n")
        self.FF_tlf.configure(text='''Flip-Flop''')
        self.ff_d7 = tk.Label(self.FF_tlf)
        self.ff_d7.place(relx=0.1, rely=0.136, height=23, width=30, bordermode='ignore')
        self.ff_d7.configure(activebackground="#f9f9f9")
        self.ff_d7.configure(anchor='w')
        self.ff_d7.configure(compound='left')
        self.ff_d7.configure(text='''D7''')
        self.ff_d6 = tk.Label(self.FF_tlf)
        self.ff_d6.place(relx=0.1, rely=0.211, height=23, width=30, bordermode='ignore')
        self.ff_d6.configure(activebackground="#f9f9f9")
        self.ff_d6.configure(anchor='w')
        self.ff_d6.configure(compound='left')
        self.ff_d6.configure(text='''D6''')
        self.ff_d5 = tk.Label(self.FF_tlf)
        self.ff_d5.place(relx=0.091, rely=0.272, height=23, width=30, bordermode='ignore')
        self.ff_d5.configure(activebackground="#f9f9f9")
        self.ff_d5.configure(anchor='w')
        self.ff_d5.configure(compound='left')
        self.ff_d5.configure(text='''D5''')
        self.ff_d4 = tk.Label(self.FF_tlf)
        self.ff_d4.place(relx=0.1, rely=0.34, height=23, width=30, bordermode='ignore')
        self.ff_d4.configure(activebackground="#f9f9f9")
        self.ff_d4.configure(anchor='w')
        self.ff_d4.configure(compound='left')
        self.ff_d4.configure(text='''D4''')
        self.ff_d3 = tk.Label(self.FF_tlf)
        self.ff_d3.place(relx=0.1, rely=0.51, height=23, width=29, bordermode='ignore')
        self.ff_d3.configure(activebackground="#f9f9f9")
        self.ff_d3.configure(anchor='w')
        self.ff_d3.configure(compound='left')
        self.ff_d3.configure(text='''D3''')
        self.ff_d2 = tk.Label(self.FF_tlf)
        self.ff_d2.place(relx=0.1, rely=0.578, height=23, width=29, bordermode='ignore')
        self.ff_d2.configure(activebackground="#f9f9f9")
        self.ff_d2.configure(anchor='w')
        self.ff_d2.configure(compound='left')
        self.ff_d2.configure(text='''D2''')
        self.ff_d1 = tk.Label(self.FF_tlf)
        self.ff_d1.place(relx=0.1, rely=0.646, height=23, width=29, bordermode='ignore')
        self.ff_d1.configure(activebackground="#f9f9f9")
        self.ff_d1.configure(anchor='w')
        self.ff_d1.configure(compound='left')
        self.ff_d1.configure(text='''D1''')
        self.ff_d0 = tk.Label(self.FF_tlf)
        self.ff_d0.place(relx=0.1, rely=0.714, height=23, width=29, bordermode='ignore')
        self.ff_d0.configure(activebackground="#f9f9f9")
        self.ff_d0.configure(anchor='w')
        self.ff_d0.configure(compound='left')
        self.ff_d0.configure(text='''D0''')
        self.ff_q7 = tk.Label(self.FF_tlf)
        self.ff_q7.place(relx=0.727, rely=0.136, height=23, width=25, bordermode='ignore')
        self.ff_q7.configure(activebackground="#f9f9f9")
        self.ff_q7.configure(anchor='w')
        self.ff_q7.configure(compound='left')
        self.ff_q7.configure(text='''Q7''')
        self.ff_q6 = tk.Label(self.FF_tlf)
        self.ff_q6.place(relx=0.727, rely=0.204, height=23, width=25, bordermode='ignore')
        self.ff_q6.configure(activebackground="#f9f9f9")
        self.ff_q6.configure(anchor='w')
        self.ff_q6.configure(compound='left')
        self.ff_q6.configure(text='''Q6''')
        self.ff_q5 = tk.Label(self.FF_tlf)
        self.ff_q5.place(relx=0.727, rely=0.272, height=23, width=25, bordermode='ignore')
        self.ff_q5.configure(activebackground="#f9f9f9")
        self.ff_q5.configure(anchor='w')
        self.ff_q5.configure(compound='left')
        self.ff_q5.configure(text='''Q5''')
        self.ff_q4 = tk.Label(self.FF_tlf)
        self.ff_q4.place(relx=0.727, rely=0.34, height=23, width=25, bordermode='ignore')
        self.ff_q4.configure(activebackground="#f9f9f9")
        self.ff_q4.configure(anchor='w')
        self.ff_q4.configure(compound='left')
        self.ff_q4.configure(text='''Q4''')
        self.ff_q3 = tk.Label(self.FF_tlf)
        self.ff_q3.place(relx=0.727, rely=0.51, height=23, width=25, bordermode='ignore')
        self.ff_q3.configure(activebackground="#f9f9f9")
        self.ff_q3.configure(anchor='w')
        self.ff_q3.configure(compound='left')
        self.ff_q3.configure(text='''Q3''')
        self.ff_q2 = tk.Label(self.FF_tlf)
        self.ff_q2.place(relx=0.727, rely=0.578, height=23, width=25, bordermode='ignore')
        self.ff_q2.configure(activebackground="#f9f9f9")
        self.ff_q2.configure(anchor='w')
        self.ff_q2.configure(compound='left')
        self.ff_q2.configure(text='''Q2''')
        self.ff_q1 = tk.Label(self.FF_tlf)
        self.ff_q1.place(relx=0.727, rely=0.646, height=23, width=25, bordermode='ignore')
        self.ff_q1.configure(activebackground="#f9f9f9")
        self.ff_q1.configure(anchor='w')
        self.ff_q1.configure(compound='left')
        self.ff_q1.configure(text='''Q1''')
        self.ff_q0 = tk.Label(self.FF_tlf)
        self.ff_q0.place(relx=0.727, rely=0.714, height=23, width=25, bordermode='ignore')
        self.ff_q0.configure(activebackground="#f9f9f9")
        self.ff_q0.configure(anchor='w')
        self.ff_q0.configure(compound='left')
        self.ff_q0.configure(text='''Q0''')
        self.ff_clk = tk.Label(self.FF_tlf)
        self.ff_clk.place(relx=0.364, rely=0.905, height=23, width=37, bordermode='ignore')
        self.ff_clk.configure(anchor='w')
        self.ff_clk.configure(compound='left')
        self.ff_clk.configure(text='''CLK''')
        self.data_tlf = ttk.Labelframe(self.top)
        self.data_tlf.place(relx=0.754, rely=0.22, relheight=0.101, relwidth=0.188)
        self.data_tlf.configure(relief='')
        self.data_tlf.configure(text='''Data''')
        self.data_entry = ttk.Entry(self.data_tlf)
        self.data_entry.place(relx=0.084, rely=0.418, relheight=0.418, relwidth=0.794, bordermode='ignore')
        #self.data_entry.configure(state='readonly')
        self.data_entry.configure(takefocus="")
        self.data_entry.configure(cursor="tcross")
        self.estado_tlf = ttk.Labelframe(self.top)
        self.estado_tlf.place(relx=0.754, rely=0.385, relheight=0.101, relwidth=0.188)
        self.estado_tlf.configure(relief='')
        self.estado_tlf.configure(text='''Estado''')
        self.estado_entry = ttk.Entry(self.estado_tlf)
        self.estado_entry.place(relx=0.093, rely=0.418, relheight=0.418, relwidth=0.794, bordermode='ignore')
        #self.estado_entry.configure(state='disabled')
        self.estado_entry.configure(takefocus="")
        self.estado_entry.configure(cursor="tcross")
        self.proxEstado_tlf = ttk.Labelframe(self.top)
        self.proxEstado_tlf.place(relx=0.754, rely=0.495, relheight=0.101, relwidth=0.188)
        self.proxEstado_tlf.configure(relief='')
        self.proxEstado_tlf.configure(text='''Prox Estado''')
        self.proxEstado_entry = ttk.Entry(self.proxEstado_tlf)
        self.proxEstado_entry.place(relx=0.084, rely=0.418, relheight=0.418, relwidth=0.794, bordermode='ignore')
        #self.proxEstado_entry.configure(state='readonly')
        self.proxEstado_entry.configure(takefocus="")
        self.proxEstado_entry.configure(cursor="tcross")
        self.archivo_tlf = ttk.Labelframe(self.top)
        self.archivo_tlf.place(relx=0.018, rely=0.0, relheight=0.101, relwidth=0.947)
        self.archivo_tlf.configure(relief='')
        self.archivo_tlf.configure(text='''Archivo''')
        self.archivo_txt = tk.Text(self.archivo_tlf)
        self.archivo_txt.place(relx=0.013, rely=0.291, relheight=0.582, relwidth=0.972, bordermode='ignore')
        self.archivo_txt.configure(background="white")
        self.archivo_txt.configure(font="TkTextFont")
        self.archivo_txt.configure(selectbackground="#c4c4c4")
        self.archivo_txt.configure(wrap="word")
        
        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.sub_menu = tk.Menu(self.menubar, activebackground='beige',activeforeground='black', tearoff=0)
        self.menubar.add_cascade(compound='left', label='Archivo',menu=self.sub_menu, )
        self.sub_menu.add_command(compound='left',label='Cargar...', command=carga_archivo)
        self.sub_menu1 = tk.Menu(self.menubar, activebackground='beige',activeforeground='black', tearoff=0)
        self.menubar.add_cascade(compound='left', label='Editar',menu=self.sub_menu1, )
        self.mi_timer=RepeatedTimer(1,evento_clock)      #creo un timer repetitivo de 1 seg de duracion

#------------------------- switches -------------
def click_sw_a7():
        global mem_a
        global mem_d
        if _w1.sw_var_a7.get():
                mem_a |=0x80
        else:
                mem_a &=~0x80
        mem_a = (mem_a & 0xF0)|(ff_q & 0x0F)
        mem_d = intelhex[mem_a]
        actualiza_board()
        return
def click_sw_a6():
        global mem_a
        global mem_d
        if _w1.sw_var_a6.get():
                mem_a |=0x40
        else:
                mem_a &=~0x40
        mem_a = (mem_a & 0xF0)|(ff_q & 0x0F)
        mem_d = intelhex[mem_a]
        actualiza_board()
        return
def click_sw_a5():
        global mem_a
        global mem_d
        if _w1.sw_var_a5.get():
                mem_a |=0x20
        else:
                mem_a &=~0x20
        mem_a = (mem_a & 0xF0)|(ff_q & 0x0F)
        mem_d = intelhex[mem_a]
        actualiza_board()
        return
def click_sw_a4():
        global mem_a
        global mem_d
        if _w1.sw_var_a4.get():
                mem_a |=0x10
        else:
                mem_a &=~0x10
        mem_a = (mem_a & 0xF0)|(ff_q & 0x0F)
        mem_d = intelhex[mem_a]
        actualiza_board()
        return
#--------------------------------------------------

def carga_archivo():
        global intelhex
        archivo=fd.askopenfilename(title="Abrir Intel Hex", filetypes=(('Intel Hex Files', '*.hex'),('Todos', '*.*')))
        _w1.archivo_txt.configure(state='normal')
        _w1.archivo_txt.delete(1.0, tk.END)
        _w1.archivo_txt.insert(1.0, archivo)
        _w1.archivo_txt.configure(state='disabled')
        intelhex = IntelHex(archivo)    # cargo el Hex 
        return

        
# --- Animo todo el show ----------
def actualiza_board():
        global mem_a
        global mem_d
        global ff_q
        global clock
        if _w1.sw_var_a7.get():
                switches_h = 0x80
        else:
                switches_h = 0
        if _w1.sw_var_a6.get():
                switches_h |=0x40
        if _w1.sw_var_a5.get():
                switches_h |=0x20
        if _w1.sw_var_a4.get():
                switches_h |=0x10
        _w1.estado_entry.delete(0, tk.END)      #borro todo lo que tiene la caja de texto
        _w1.estado_entry.insert(0,mem_a)        # y escribo la variable de estado 
        _w1.proxEstado_entry.delete(0, tk.END)      #borro todo lo que tiene la caja de texto
        _w1.proxEstado_entry.insert(0,(mem_d & 0x0F)|(switches_h)) # y escribo la variable de proximo estado
        _w1.data_entry.delete(0, tk.END)      #borro todo lo que tiene la caja de texto
        _w1.data_entry.insert(0,ff_q) # y escribo la variable de proximo estado
        
        if clock==1:
                _w1.clock_led.configure(style="LedAmOn.TFrame") # enciendo LED de clock
                _w1.ff_clk.configure(background=_bg_amarillo)   # enciendo label de clock
        else:
                _w1.clock_led.configure(style="LedAmOff.TFrame") # apago led de clock
                _w1.ff_clk.configure(background=_bgcolor)   # apago label de clock 

# ------------------------ mem_a ----------------------------------
        if(mem_a & 1)!=0:
                _w1.mem_a0.configure(background=_bg_rojo_on)
        else:
                _w1.mem_a0.configure(background=_bgcolor)
        if(mem_a & 2)!=0:
                _w1.mem_a1.configure(background=_bg_rojo_on)
        else:
                _w1.mem_a1.configure(background=_bgcolor)
        if(mem_a & 4)!=0:
                _w1.mem_a2.configure(background=_bg_rojo_on)
        else:
                _w1.mem_a2.configure(background=_bgcolor)
        if(mem_a & 8)!=0:
                _w1.mem_a3.configure(background=_bg_rojo_on)
        else:
                _w1.mem_a3.configure(background=_bgcolor)
        if(mem_a & 0x10)!=0:
                _w1.mem_a4.configure(background=_bg_rojo_on)
        else:
                _w1.mem_a4.configure(background=_bgcolor)
        if(mem_a & 0x20)!=0:
                _w1.mem_a5.configure(background=_bg_rojo_on)
        else:
                _w1.mem_a5.configure(background=_bgcolor)
        if(mem_a & 0x40)!=0:
                _w1.mem_a6.configure(background=_bg_rojo_on)
        else:
                _w1.mem_a6.configure(background=_bgcolor)
        if(mem_a & 0x80)!=0:
                _w1.mem_a7.configure(background=_bg_rojo_on)
        else:
                _w1.mem_a7.configure(background=_bgcolor)
#------------------------ mem data -----------------------------
        if(mem_d & 1)!=0:
                _w1.ff_d0.configure(background=_bg_rojo_on)
                _w1.mem_d0.configure(background=_bg_rojo_on)
        else:
                _w1.ff_d0.configure(background=_bgcolor)
                _w1.mem_d0.configure(background=_bgcolor)
        if(mem_d & 2)!=0:
                _w1.ff_d1.configure(background=_bg_rojo_on)
                _w1.mem_d1.configure(background=_bg_rojo_on)
        else:
                _w1.ff_d1.configure(background=_bgcolor)
                _w1.mem_d1.configure(background=_bgcolor)
        if(mem_d & 4)!=0:
                _w1.ff_d2.configure(background=_bg_rojo_on)
                _w1.mem_d2.configure(background=_bg_rojo_on)
        else:
                _w1.ff_d2.configure(background=_bgcolor)
                _w1.mem_d2.configure(background=_bgcolor)
        if(mem_d & 8)!=0:
                _w1.ff_d3.configure(background=_bg_rojo_on)
                _w1.mem_d3.configure(background=_bg_rojo_on)
        else:
                _w1.ff_d3.configure(background=_bgcolor)
                _w1.mem_d3.configure(background=_bgcolor)
        if(mem_d & 0x10)!=0:
                _w1.ff_d4.configure(background=_bg_verde_on)
                _w1.mem_d4.configure(background=_bg_verde_on)
        else:
                _w1.ff_d4.configure(background=_bgcolor)
                _w1.mem_d4.configure(background=_bgcolor)
        if(mem_d & 0x20)!=0:
                _w1.ff_d5.configure(background=_bg_verde_on)
                _w1.mem_d5.configure(background=_bg_verde_on)
        else:
                _w1.ff_d5.configure(background=_bgcolor)
                _w1.mem_d5.configure(background=_bgcolor)
        if(mem_d & 0x40)!=0:
                _w1.ff_d6.configure(background=_bg_verde_on)
                _w1.mem_d6.configure(background=_bg_verde_on)
        else:
                _w1.ff_d6.configure(background=_bgcolor)
                _w1.mem_d6.configure(background=_bgcolor)
        if(mem_d & 0x80)!=0:
                _w1.ff_d7.configure(background=_bg_verde_on)
                _w1.mem_d7.configure(background=_bg_verde_on)
        else:
                _w1.ff_d7.configure(background=_bgcolor)
                _w1.mem_d7.configure(background=_bgcolor)
                
#---------------------- next data --------------------------                
        if(ff_q & 1)!=0:
                _w1.ff_q0.configure(background=_bg_rojo_on)
        else:
                _w1.ff_q0.configure(background=_bgcolor)
        if(ff_q & 2)!=0:
                _w1.ff_q1.configure(background=_bg_rojo_on)
        else:
                _w1.ff_q1.configure(background=_bgcolor)
        if(ff_q & 4)!=0:
                _w1.ff_q2.configure(background=_bg_rojo_on)
        else:
                _w1.ff_q2.configure(background=_bgcolor)
        if(ff_q & 8)!=0:
                _w1.ff_q3.configure(background=_bg_rojo_on)
        else:
                _w1.ff_q3.configure(background=_bgcolor)
        if(ff_q & 0x10)!=0:
                _w1.ff_q4.configure(background=_bg_verde_on)
        else:
                _w1.ff_q4.configure(background=_bgcolor)
        if(ff_q & 0x20)!=0:
                _w1.ff_q5.configure(background=_bg_verde_on)
        else:
                _w1.ff_q5.configure(background=_bgcolor)
        if(ff_q & 0x40)!=0:
                _w1.ff_q6.configure(background=_bg_verde_on)
        else:
                _w1.ff_q6.configure(background=_bgcolor)
        if(ff_q & 0x80)!=0:
                _w1.ff_q7.configure(background=_bg_verde_on)
        else:
                _w1.ff_q7.configure(background=_bgcolor)
                
        return

##-------- clase timer para poder realizar intervalos ---------
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self._timer     = None
        #self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        if self.is_running:
            self._timer.cancel()
            self.is_running = False


# --------------------- Boton Run/Stop --------------------
def click_run_stop_button(evento): 
        global corriendo
        if corriendo==0:#
                _w1.run_stop_button.configure(text='''Stop''')
                corriendo=1
                _w1.mi_timer.start()
        else:
                _w1.run_stop_button.configure(text='''Run''')
                corriendo=0
                _w1.mi_timer.stop()
        return

# ------------------- Boton de Reset -----------------------
def click_reset_button(evento):
        global ff_q
        global mem_a
        global mem_d
        global memoria
        global clock
        global corriendo
        clock=0
        corriendo=0
        ff_q = 0
        if _w1.sw_var_a7.get():
                mem_a = 0x80
        else:
                mem_a = 0
        if _w1.sw_var_a6.get():
                mem_a |=0x40
        if _w1.sw_var_a5.get():
                mem_a |=0x20
        if _w1.sw_var_a4.get():
                mem_a |=0x10
        #mem_d = memoria[mem_a] #obtengo datos de la memoria hardcoded
        mem_d = intelhex[mem_a]
        _w1.clock_led.configure(style="LedAmOff.TFrame") # apago led de clock
        _w1.ff_clk.configure(background=_bgcolor)   # apago label de clock
        _w1.mi_timer.stop()
        _w1.run_stop_button.configure(text='''Run''')
        actualiza_board()
        return

# ---------- Funcion de timer/clock -------------------------
def evento_clock():
        global clock
        global mem_a
        global mem_d
        global ff_q
        if clock==0:
                ff_q=mem_d;
                mem_a = (mem_a & 0xF0)|(ff_q & 0x0F)
                mem_d = intelhex[mem_a]
                #mem_d = memoria[mem_a]
                clock=1;
        else:
                clock=0;
        
        actualiza_board()
        return

# -------------------- MAIN --------------------
def main(*args):
    try:
        '''Main entry point '''
        global root
        global ff_q
        global mem_a
        global mem_d
        global memoria
        global clock
        
        root = tk.Tk()
        root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
        # Creo toplevel widget.
        global _top1, _w1
        _top1 = root
        _w1 = machinemulator(_top1)
        #_w1.mi_timer.stop()    #esto no anda por que aun no esta declarado timer
        
        _w1.run_stop_button.bind('<Button-1>', click_run_stop_button)        #bindeo la funcion click_run.. con el evento click boton izquierdo
        _w1.reset_button.bind('<Button-1>', click_reset_button)
        
        _w1.clock_led.configure(style="LedAmOff.TFrame") # apago led de clock
        _w1.ff_clk.configure(background=_bgcolor)   # apago label de clock
        clock=0
        
        _w1.run_stop_button.configure(text='''Run''')
        ff_q=0
        mem_a=0
        mem_d = memoria[mem_a]
        actualiza_board()
        
        root.mainloop()
        
    finally:    # se ejecuta cuando se cierra el programa
        _w1.mi_timer.stop()
        clock=0


if __name__ == '__main__':      #corro main si es el main
    main()


