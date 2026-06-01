import flet as ft

class ZRQChatApp:
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
            ft.Text("ZRQ Chat", size=20, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
            ft.IconButton(icon=ft.icons.SEARCH_ROUNDED, icon_color=ft.colors.GREY_400)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # Список активных чатов (Компоненты)
        def create_chat_item(title, last_msg, time, unread_count=0):
            return ft.Container(
                content=ft.Row([
                    ft.CircleAvatar(
                        content=ft.Text(title[0], color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
                        bgcolor=ft.colors.BLUE_ACCENT
                    ),
                    ft.VerticalDivider(width=5, color=ft.colors.TRANSPARENT),
                    ft.Expanded(
                        child=ft.Column([
                            ft.Text(title, size=16, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
                            ft.Text(last_msg, size=13, color=ft.colors.GREY_400, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS)
                        ], spacing=2, alignment=ft.MainAxisAlignment.CENTER)
                    ),
                    ft.Column([
                        ft.Text(time, size=11, color=ft.colors.GREY_500),
                        ft.Container(
                            content=ft.Text(str(unread_count), size=10, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD) if unread_count > 0 else ft.Text(""),
                            bgcolor=ft.colors.BLUE_ACCENT if unread_count > 0 else ft.colors.TRANSPARENT,
                            padding=5,
                            border_radius=10,
                            alignment=ft.alignment.center
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=5)
                ]),
                padding=10,
                border_radius=12,
                bgcolor="#1E2022"
            )

        chat_list = ft.Column([
            ft.Text("АКТИВНЫЕ ДИАЛОГИ", size=12, color=ft.colors.GREY_500, weight=ft.FontWeight.BOLD),
            create_chat_item("Главный Архитектор", "Пулл-реквест одобрен, собираем билд в APK.", "16:54", unread_count=1),
            create_chat_item("DevOps Core", "Vercel проксирует запросы к Supabase стабильно.", "12:01"),
            create_chat_item("ZRQ Bot", "Региональный этап завершен успешно.", "Вчера")
        ], spacing=10)

        return ft.Container(
            content=ft.Column([
                app_bar,
                ft.VerticalDivider(height=10, color=ft.colors.TRANSPARENT),
                chat_list
            ], scroll=ft.ScrollMode.AUTO),
            padding=20,
            expand=True
        )
