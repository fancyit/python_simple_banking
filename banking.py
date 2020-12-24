from menu import MainMenu

m = MainMenu()
m.print_menu()
option = int(input())

while option != 0:
    m.menu_options(option)
    option = int(input())