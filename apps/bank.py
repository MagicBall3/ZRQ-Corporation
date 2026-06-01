import flet as ft

class ZRQBankApp:
    def __init__(self, nav_manager):
        self.nav_manager = nav_manager

    def build(self):
        # Панель навигации (Назад)
        app_bar = ft.Row([
            ft.IconButton(
                icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED,
                icon_color=ft.colors.WHITE,
                icon_size=18,
                on_click=lambda e: self.nav_manager.go_back()
            ),
            ft.Text("ZRQ Bank", size=20, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
            ft.IconButton(icon=ft.icons.INFO_OUTLINED, icon_color=ft.colors.GREY_400)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # Баланс пользователя
        balance_card = ft.Container(
            content=ft.Column([
                ft.Text("Текущий баланс", size=12, color=ft.colors.GREEN_100),
                ft.Text("1,250,500 ZRQ", size=32, color=ft.colors.WHITE, weight=ft.FontWeight.W_900),
                ft.Row([
                    ft.Text("Премиум аккаунт", size=11, color=ft.colors.GREEN_ACCENT),
                    ft.Icon(ft.icons.VERIFIED_ROUNDED, color=ft.colors.GREEN_ACCENT, size=14)
                ], spacing=5)
            ], alignment=ft.MainAxisAlignment.CENTER),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#0A361B", "#115C2E"]
            ),
            padding=25,
            border_radius=20,
            margin=ft.margin.only(top=10, bottom=20)
        )

        # Заглушка списка транзакций
        transactions = ft.Column([
            ft.Text("ПОСЛЕДНИЕ ОПЕРАЦИИ", size=12, color=ft.colors.GREY_500, weight=ft.FontWeight.BOLD),
            ft.ListTile(
                leading=ft.Icon(ft.icons.ARROW_DOWNWARD_ROUNDED, color=ft.colors.GREEN_ACCENT),
                title=ft.Text("Пополнение от Vercel_API_Gate", color=ft.colors.WHITE),
                subtitle=ft.Text("Сегодня, 14:23", color=ft.colors.GREY_500),
                trailing=ft.Text("+15,000 ZRQ", color=ft.colors.GREEN_ACCENT, weight=ft.FontWeight.BOLD)
            ),
            ft.ListTile(
                leading=ft.Icon(ft.icons.ARROW_UPWARD_ROUNDED, color=ft.colors.RED_ACCENT),
                title=ft.Text("Оплата хостинга ноды", color=ft.colors.WHITE),
                subtitle=ft.Text("Вчера, 23:11", color=ft.colors.GREY_500),
                trailing=ft.Text("-4,200 ZRQ", color=ft.colors.RED_ACCENT, weight=ft.FontWeight.BOLD)
            )
        ], spacing=10)

        return ft.Container(
            content=ft.Column([
                app_bar,
                balance_card,
                transactions
            ], scroll=ft.ScrollMode.AUTO),
            padding=20,
            expand=True
        )
