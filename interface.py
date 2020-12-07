from tkinter.constants import CENTER
from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox

class interf:
    HEIGHT = 500
    WIDTH = 600
    value = 0
    texto = None

    def draw_screen(self, root):
        canvas = tk.Canvas(root, height=self.HEIGHT, width=self.WIDTH, bg='#ADD8E6')
        canvas.pack()

    def format_response(self, classe):
        try:
            final_str = "Essa casa está classificada como: " + classe
        except:
            final_str = 'Erro na classificação'

        self.label.config(text = final_str)
        self.texto = final_str

        return final_str

    def get_value(self, value, entry, root):
        self.value = value
        entry.delete(0)
        root.quit()

    def new_check(self, root):
        self.value = 1
        self.label.config(text = None) 
        self.texto = None
        root.quit()

    def on_closing(self, root):
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            root.destroy()
        
    def traduzir(self, no):
        if no == 'sqft_living': 
            return 'Por favor digite a área da casa'
        elif no == 'price': 
            return 'Por favor digite o preço ofertado'
        elif no == 'sqft_lot': 
            return 'Por favor digite a área do lote/terreno'
        elif no == 'sqft_basement': 
            return 'Por favor digite a área do porão'
        else:
            return None

    def validar(self, S):
        if S.isdigit():
            return True
        else:
            return False

    def show(self, root, classe, no):
        no = self.traduzir(no)

        msg = tk.Frame(root, bg='#ADD8E6', bd=5)
        msg.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

        dado = tk.Label(msg)
        dado.place(relwidth=1, relheight=1)
        if classe == None:
            dado['text'] = no

        frame = tk.Frame(root, bg='#ADD8E6', bd=5)
        frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.1, anchor='n')

        entry = tk.Entry(frame, font=40, validate="key")
        entry['validatecommand'] = (entry.register(self.validar),'%S')
        entry.place(relwidth=0.35, relheight=1)

        button = tk.Button(frame, text="Enviar", font=40, command=lambda: self.get_value(entry.get(), entry, root))
        button.place(relx=0.5, relheight=1, relwidth=0.25, anchor='n')

        button_clean = tk.Button(frame, text="Limpar", font=40, command=lambda: entry.delete(0, 'end'))
        button_clean.place(relx=0.8, relheight=1, relwidth=0.25, anchor='n')

        lower_frame = tk.Frame(root, bg='#ADD8E6', bd=5)
        lower_frame.place(relx=0.5, rely=0.40, relwidth=0.7, relheight=0.1, anchor='n')

        lframe2 = tk.Frame(root, bg='#ADD8E6', bd=5)
        lframe2.place(relx=0.1, rely=0.60, relwidth=1.5, relheight=0.1, anchor='n')

        button_new = tk.Button(lframe2, text="Nova Consulta", font=40, command=lambda: self.new_check(root))
        button_new.place(relx=0.60, relheight=1, relwidth=0.25, anchor='n')

        button_close = tk.Button(lframe2, text="Encerrar", font=40, command=lambda: self.on_closing(root))
        button_close.place(relx=0.90, relheight=1, relwidth=0.25, anchor='n')

        self.label = tk.Label(lower_frame, text=self.texto)
        self.label.place(relwidth=1, relheight=1)
        if len(self.label.cget('text')) <= 1:
            entry.focus_set()
        else:
            entry.config(state=DISABLED)

        root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(root))
        root.mainloop()

        return float(self.value)