import flet as ft

class NavigationManager:
    def __init__(self, page: ft.Page):
        self.page = page
        self.history = []  # Стек для хранения истории экранов (экземпляров классов)

    def navigate_to(self, screen_instance):
        """Переход на новый экран. Добавляет его в стек и отрисовывает."""
        if self.history:
            # Скрываем или деактивируем текущий экран, если необходимо
            pass
        self.history.append(screen_instance)
        self._render_current()

    def go_back(self):
        """Возврат на предыдущий экран. Уничтожает текущий."""
        if len(self.history) > 1:
            self.history.pop()  # Удаляем текущий экран из стека
            self._render_current()
        else:
            # Если это последний экран (ZRQ Store), закрываем приложение
            self.page.window_close()

    def _render_current(self):
        """Очищает страницу и строит интерфейс текущего экрана."""
        self.page.controls.clear()
        current_screen = self.history[-1]
        
        # Строим UI экрана и добавляем его на страницу
        ui_content = current_screen.build()
        self.page.add(ui_content)
        self.page.update()
