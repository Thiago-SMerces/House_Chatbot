from generated_tree_gui import Tree
import tkinter as tk
from interface import interf

t = Tree()
continua = None
root = tk.Tk()
inte = interf()
inte.draw_screen(root)
root.title("Chatbot para estimar preços de casas no CEP 98106")

while continua != 0:
    continua = t.decision(root, inte)
