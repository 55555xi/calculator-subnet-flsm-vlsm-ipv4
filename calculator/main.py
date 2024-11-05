# main.py
import importlib
import os
import time
from colorama import Fore, Style, init

init(autoreset=True)

class Colors:
    COLORS = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    CYAN = Fore.CYAN  #primer color
    RESET = Style.RESET_ALL #reset para el rainbow

art = """
                     Subnet Wizard                       
                     -------------                       
                 ___====-_  _-====___
           _--^^^#####//      \\#####^^^--_
        _-^##########// (    ) \\##########^-_
       -############//  |\\^^/|  \\############-
     _/############//   (@::@)   \\############\\_
    /#############((     \\\\//     ))#############\\
   -###############\\\\    (oo)    //###############-
  -#################\\\\  / VV \\  //#################-
 -###################\\\\/      \\/###################-
 _#/|##########/\\######(   /\\   )######/\\##########|\\#_
 |/ |#/\\#/\\#/\\/  \\#/\\##\\  |  |  /##/\\#/  \\/\\#/\\#/\\#| \\|
 `  |/  V  V  `   V  \\#\\| |  | |/#/  V   '  V  V  \\|  '
    `   `  `      `   / | |  | | \\   '      '  '   '
                    (  | |  | |  )
                   __\\ | |  | | /__
                  (vvv(VVV)(VVV)vvv)
"""

new_logo = """
███╗   ███╗████████╗███████╗███╗   ███╗ ██████╗  ██╗
████╗ ████║╚══██╔══╝██╔════╝████╗ ████║██╔═████╗███║
██╔████╔██║   ██║   █████╗  ██╔████╔██║██║██╔██║╚██║
██║╚██╔╝██║   ██║   ██╔══╝  ██║╚██╔╝██║████╔╝██║ ██║
██║ ╚═╝ ██║   ██║   ██║     ██║ ╚═╝ ██║╚██████╔╝ ██║
╚═╝     ╚═╝   ╚═╝   ╚═╝     ╚═╝     ╚═╝ ╚═════╝  ╚═╝
"""

def clear_screen():
    """Limpia la pantalla según el sistema operativo."""
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_colors(duration=4):
    """Anima los colores del arte ASCII durante un tiempo limitado."""
    start_time = time.time()
    color_index = 0

    while time.time() - start_time < duration:
        clear_screen()
        color = Colors.COLORS[color_index % len(Colors.COLORS)]
        print(color + art + Colors.RESET)
        time.sleep(0.3)
        color_index += 1

def show_new_logo():
    """Muestra el nuevo logo grande."""
    clear_screen()
    print(Colors.CYAN + new_logo + Colors.RESET)
    time.sleep(2)  # Espera 2 segundos antes de continuar

def run_calculator(calculator_module, function_name):
    """Ejecuta una calculadora y ofrece opción para repetir o volver al menú."""
    while True:
        getattr(calculator_module, function_name)()
        choice = input("\n¿Desea ejecutar esta calculadora de nuevo? (s/n): ").strip().lower()
        if choice != 's':
            break

def main_menu():
    """Menú principal para seleccionar la calculadora."""
    while True:
        print("\nSeleccione una opción:")
        print("1 - Calculadora VLSM")
        print("2 - Calculadora FLSM")
        print("3 - Calculadora IPv4")
        print("4 - Salir")

        option = input("Ingrese su opción (1/2/3/4): ")

        if option == '1':
            try:
                vlsm_calculator = importlib.import_module("vlsm_calculadora")
                run_calculator(vlsm_calculator, "main")
            except ModuleNotFoundError:
                print("Error: No se pudo encontrar 'vlsm_calculadora.py'")
        elif option == '2':
            try:
                flsm_calculator = importlib.import_module("flsm_calculadora")
                run_calculator(flsm_calculator, "main")
            except ModuleNotFoundError:
                print("Error: No se pudo encontrar 'flsm_calculadora.py'")
        elif option == '3':
            try:
                ipv4_calculator = importlib.import_module("ipv4_calculadora")
                run_calculator(ipv4_calculator, "ipv4_calculadora")
            except ModuleNotFoundError:
                print("Error: No se pudo encontrar 'ipv4_calculadora.py'")
        elif option == '4':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, elija 1, 2, 3 o 4.")

if __name__ == "__main__":
    animate_colors(duration=4)  # Anima los colores durante 4 segundos
    show_new_logo()  # Muestra el nuevo logo grande
    main_menu()  # Muestra el menú principal
