from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from urllib.parse import parse_qs


class MyWebServer(BaseHTTPRequestHandler):

    # 1. Этот метод отвечает за отображение самой страницы (как и раньше)
    def do_GET(self):
        html_filename = "21-2_home4.html"

        if not os.path.exists(html_filename):
            self.send_response(404)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"Ошибка: Файл '{html_filename}' не найден!".encode("utf-8"))
            return

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        with open(html_filename, "r", encoding="utf-8") as file:
            html_content = file.read()

        self.wfile.write(bytes(html_content, "utf-8"))

    # 2. НОВЫЙ МЕТОД: Обрабатывает отправку формы контактов
    def do_POST(self):
        if self.path == "/submit-contacts":
            # Определяем длину входящих данных
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            # Парсим полученные из полей формы данные
            parsed_data = parse_qs(post_data)

            # Получаем чистые значения полей (из тегов name="name", name="email" и т.д.)
            user_name = parsed_data.get('name', [''])[0]
            user_email = parsed_data.get('email', [''])[0]
            user_message = parsed_data.get('message', [''])[0]

            # Выводим полученные данные в терминал PyCharm для проверки
            print("\n" + "=" * 30)
            print("ПОЛУЧЕНЫ ДАННЫЕ ИЗ ФОРМЫ:")
            print(f"Имя: {user_name}")
            print(f"Почта: {user_email}")
            print(f"Сообщение: {user_message}")
            print("=" * 30 + "\n")

            # Отправляем ответ пользователю об успешной отправке
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            # Создаем простую HTML-страничку ответа с кнопкой возврата назад
            success_html = f"""
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <title>Успешно отправлено</title>
                <link href="https://jsdelivr.net" rel="stylesheet">
            </head>
            <body class="bg-light d-flex align-items-center justify-content-center" style="height: 100vh;">
                <div class="card p-5 shadow-sm text-center" style="max-width: 500px;">
                    <div class="text-success display-1 mb-3">✓</div>
                    <h2 class="fw-normal mb-3">{user_name}, спасибо!</h2>
                    <p class="text-secondary mb-4">Ваше сообщение успешно отправлено на сервер.</p>
                    <a href="/" class="btn btn-primary px-4">Назад к контактам</a>
                </div>
            </body>
            </html>
            """
            self.wfile.write(bytes(success_html, "utf-8"))


def run(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MyWebServer)
    print(f"==================================================")
    print(f" Сервер перезапущен и готов к обработке форм!")
    print(f" Откройте в браузере ссылку: http://localhost:{port}")
    print(f"==================================================")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")


if __name__ == "__main__":
    run()
