import flet as ft

class ZRQStoreApp:
    def __init__(self, nav_manager):
        self.nav_manager = nav_manager

    def build(self):
        # Хедер магазина
        header = ft.Container(
            content=ft.Column([
                ft.Text("ZRQ Corp", size=14, color=ft.colors.BLUE_ACCENT, weight=ft.FontWeight.BOLD, letter_spacing=2),
                ft.Text("ECOSYSTEM HUB", size=28, color=ft.colors.WHITE, weight=ft.FontWeight.W_900),
                ft.Text("Добро пожаловать в цифровое пространство ZRQ", size=12, color=ft.colors.GREY_500)
            ], spacing=2),
            padding=ft.padding.only(top=20, bottom=20)
        )

        # Компонент карточки для запуска суб-приложений
        def create_app_card(title, description, icon, color, on_click_action):
            return ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(icon, color=color, size=30),
                        bgcolor=ft.colors.with_opacity(0.1, color),
                        padding=15,
                        border_radius=12
                    ),
                    ft.VerticalDivider(width=10, color=ft.colors.TRANSPARENT),
                    ft.Expanded(
                        child=ft.Column([
                            ft.Text(title, size=18, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
                            ft.Text(description, size=12, color=ft.colors.GREY_400, max_lines=2)
                        ], spacing=4, alignment=ft.MainAxisAlignment.CENTER)
                    ),
                    ft.Icon(ft.icons.ARROW_FORWARD_IOS_ROUNDED, color=ft.colors.GREY_600, size=16)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                bgcolor="#1A1C1E",
                padding=20,
                border_radius=16,
                border=ft.border.all(1, "#2C2F33"),
                on_click=on_click_action,
                animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT)
            )

        # Инициализация переходов
        def open_bank(e):
            from apps.bank import ZRQBankApp
            self.nav_manager.navigate_to(ZRQBankApp(self.nav_manager))

        def open_chat(e):
            from apps.chat import ZRQChatApp
            self.nav_manager.navigate_to(ZRQChatApp(self.nav_manager))

        # Сетка доступных приложений
        apps_grid = ft.Column([
            create_app_card(
                "ZRQ Bank", 
                "Управление внутренними счетами, транзакции и безопасность активов Corp.", 
                ft.icons.ACCOUNT_BALANCE_WALLET_ROUNDED, 
                ft.colors.GREEN_ACCENT, 
                open_bank
            ),
            create_app_card(
                "ZRQ Chat", 
                "Зашифрованный корпоративный мессенджер для связи внутри экосистемы.", 
                ft.icons.CHAT_BUBBLE_ROUNDED, 
                ft.colors.BLUE_ACCENT, 
                open_chat
            )
        ], spacing=15)

        # Финальный контейнер экрана Store
        return ft.Container(
            content=ft.Column([
                header,
                ft.Divider(height=1, color="#2C2F33"),
                ft.VerticalDivider(height=10, color=ft.colors.TRANSPARENT),
                ft.Text("ДОСТУПНЫЕ СЕРВИСЫ", size=12, color=ft.colors.GREY_500, weight=ft.FontWeight.BOLD, letter_spacing=1),
                ft.VerticalDivider(height=5, color=ft.colors.TRANSPARENT),
                apps_grid
            ], scroll=ft.ScrollMode.AUTO),
            padding=20,
            expand=True
        )
