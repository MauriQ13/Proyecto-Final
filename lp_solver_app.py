#!/usr/bin/env python3
"""
Script principal de la aplicación de Programación Lineal.
Este es el punto de entrada único que inicializa y ejecuta la aplicación.

Autor: Proyecto Final
Versión: 1.0.0
Descripción: Aplicación de escritorio para resolver problemas de Programación Lineal
             con 2 variables de decisión y 3 restricciones usando PuLP y Tkinter.
"""

import tkinter as tk
from src.ui.main_window import LPSolverGUI


def main():
    """
    Función principal que inicializa y ejecuta la aplicación.
    """
    # Crear la ventana principal
    root = tk.Tk()
    
    # Inicializar la aplicación
    app = LPSolverGUI(root)
    
    # Ejecutar el loop principal de la aplicación
    root.mainloop()


if __name__ == "__main__":
    main()
