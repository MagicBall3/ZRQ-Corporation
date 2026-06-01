import flet as ft
from core.navigation import NavigationManager
from apps.store import ZRQStoreApp

def main(page: ft.Page):
    # Глобальные настройки окна/экрана под мобильное устройство
    page.title = "ZRQ Store SuperApp"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#121314"  # Фирменный глубокий темный цвет
    page.padding = 0

    # Настройка темы Flet UI для инпутов и шрифтов
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.colors.BLUE_ACCENT,
            background="#121314",
            surface="#1A1C1E"
        )
    )

    # Инициализация единого менеджера навигации
    nav_manager = NavigationManager(page)

    # Перехват системного события закрытия/возврата (актуально для APK на Android)
    def on_back_button_pressed(e):
        # Если ОС или окружение пытается вызвать pop, используем наш менеджер стека
        e.prevent_default = True
        nav_manager.go_back()

    # Связываем обработчик возврата
    page.on_view_pop = on_back_button_pressed

    # Точка старта: Загружаем ZRQ Store как корневой экран системы
    store_home = ZRQStoreApp(nav_manager)
    nav_manager.navigate_to(store_home)

# Запуск приложения
if __name__ == "__main__":
    ft.app(target=main)
