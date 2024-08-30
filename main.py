from Controls.controls import (
    Calendario,
    ft
)

def main(page: ft.Page):
    page.title = 'Calendario'
    page.window.maximized = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER  

    calendar = Calendario()

    page.add(calendar)

if __name__ == '__main__':
    ft.app(target=main)
