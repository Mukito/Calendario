import flet as ft
from datetime import datetime
import calendar



class Calendario(ft.Container):
    def __init__(
            self
    ):
        self.meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        self.anos = [ano for ano in range(1900, 2101, 1)]
        
        # Obter a data atual
        day, month, year = self.current_date

        super().__init__()
        self.width = 250
        self.height = 340
        self.bgcolor = ft.colors.WHITE
        self.border_radius = 8
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=150,
            color=ft.colors.BLACK,
            offset=ft.Offset(x=0, y=0),
            blur_style=ft.ShadowBlurStyle.NORMAL
            
        )
        self.padding = ft.padding.all(10)
        self.content = ft.Column(
            # aqui foi copiado o codigo
            controls=[
                ft.Row(
                    controls=[
                        DateSetField(
                            value=self.meses[month - 1],
                            options=[
                                ft.dropdown.Option(text=mes) for mes in self.meses
                            ],
                            width=90,
                            on_change=lambda e: self.fill_days(e)
                        ),
                        DateSetField(
                            #value=self.anos,
                            value=year,
                            options=[
                                ft.dropdown.Option(text=ano) for ano in self.anos
                            ],
                            width=60,
                            on_change=lambda e: self.fill_days(e)
                        ),
                        Buttons(
                            icon=ft.icons.KEYBOARD_ARROW_DOWN,
                            on_click=lambda e: self.next_date(e)
                        ),
                        Buttons(
                            icon=ft.icons.KEYBOARD_ARROW_UP,
                            on_click=lambda e: self.previous_date(e)
                        )
                    ],
                    spacing=8
                ),
                #coloca os dias da semana
                ft.Row(
                    controls=[
                        DateShowDays( 
                            value=value 
                        ) for value in ['S', 'T', 'Q', 'Q', 'S', 'S', 'D']
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                #coloca os quadrados em baixo
                ft.Row(
                    controls=[
                        DateShowDays(
                            value=''
                        ) for _ in range(42)
                    ],
                    wrap=True,
                    spacing=3.3
                )
            ],
            #espaçamento
            spacing=5
        )
        
        self.fill_days()
        self.change_color()

    @property
    def current_date(self) -> tuple[int, int, int]:
        day, month, year = datetime.now().strftime('%d/%m/%Y').split('/')
        return int(day), int(month), int(year)

    @property
    def filled_date(self) -> tuple[str, int]:
        month: str = str(self.content.controls[0].controls[0].value)
        year: int = int(self.content.controls[0].controls[1].value)    
        
        return month, year

    @property
    def month_days(self):
        month, year = self.filled_date

        first_day, total_month_days = calendar.monthrange(year=year, month=(self.meses.index(month)+1))

        return first_day, total_month_days
    
    @property
    def clear_content(self):
        for i in range(42):
            self.content.controls[2].controls[i].content.value = ''
    
    def change_color(self, e: ft.ControlEvent = None):
        day, month, year = self.current_date
        fill_month, fill_year = self.filled_date

        print(self.meses.index(fill_month))

        if year == fill_year and (month == self.meses.index(fill_month) + 1):
            for i in range(42):
                if self.content.controls[2].controls[i].content.value == str(day):
                    self.content.controls[2].controls[i].bgcolor = ft.colors.BLUE
                    self.content.controls[2].controls[i].content.color = ft.colors.WHITE
                    break    

        else:
            for i in range(42):
                self.content.controls[2].controls[i].bgcolor = ft.colors.TRANSPARENT
                self.content.controls[2].controls[i].content.color = ft.colors.GREEN

        try:
            self.page.update()

        except:
            pass



    def fill_days(self, e: ft.ControlEvent = None):
        first_day, month_days = self.month_days
        self.clear_content

        for day in range(1, month_days + 1):
            self.content.controls[2].controls[first_day + day - 1].content.value = day

        try:
            self.page.update()

        except:
            pass    

        #print(self.filled_date[0], first_day, month_days)


    def next_date(self, e: ft.ControlEvent):
        month, year = self.filled_date    #Acessar como atributo, não método
        #self.clear_content

        if self.meses.index(month) < 11:
            self.content.controls[0].controls[0].value = self.meses[self.meses.index(month) + 1]
        
        else:
            self.content.controls[0].controls[0].value = self.meses[0]
            self.content.controls[0].controls[1].value = year + 1

        self.fill_days()
        self.change_color()
        self.page.update()   # Atualiza o container     
        

    def previous_date(self, e: ft.ControlEvent):
        month, year = self.filled_date    #Acessar como atributo, não método
        #self.clear_content

        if self.meses.index(month) > 0:
            self.content.controls[0].controls[0].value = self.meses[self.meses.index(month) - 1]
        
        else:
            self.content.controls[0].controls[0].value = self.meses[11]
            self.content.controls[0].controls[1].value = year - 1

        self.fill_days()
        self.change_color()
        self.page.update()    #Atualiza o container
        



class DateSetField(ft.Dropdown):
    def __init__(
            self,
            value: str,
            options: list[ft.dropdown.Option],
            width: float,
            on_change: ft.ControlEvent = None
    ):
        super().__init__()
        self.width = width
        self.height = 50
        self.on_change = on_change
        self.border = ft.InputBorder.NONE
        self.options = options
        self.value = value
        self.color = ft.colors.GREEN
        self.text_style = ft.TextStyle(
            weight='bold', 
            size=14
        )

class Buttons(ft.Container):
    def __init__(
        self,
        icon: ft.icons,
        on_click: ft.ControlEvent = None
    ):
        super().__init__()
        self.width = 30
        self.height = 30
        
        self.border_radius = 30
        self.content = ft.Icon(
            name=icon,
            color=ft.colors.GREEN,
            size=18
        )
        self.alignment = ft.alignment.center
        self.on_click = on_click

class DateShowDays(ft.Container):
    def __init__(
        self,
        value: str
    ):
        super().__init__()
        self.width = 210 / 7
        self.height = 210 / 7
        self.border_radius = 2
        self.border = ft.border.all(
            width=1,
            color=ft.colors.GREEN
        )

        self.content = ft.Text(
            value=value,
            color=ft.colors.GREEN,
            size=14,
            weight='bold',
            text_align=ft.TextAlign.CENTER
        )
        self.alignment = ft.alignment.center
         

