from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from urllib.parse import parse_qs


class MyWebServer(BaseHTTPRequestHandler):

    def do_GET(self):
        # 1. Если кликнули на корень http://localhost:8000/, открываем главную
        if self.path == "/":
            html_filename = "21-2_home1.html"
        else:
            # Отрезаем параметры кэша (все, что после знака вопроса)
            clean_path = self.path.split('?')[0]
            html_filename = clean_path.lstrip("/")

        # 2. Проверяем, существует ли такой HTML-файл в папке проекта
        if os.path.exists(html_filename) and html_filename.endswith(".html"):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            with open(html_filename, "r", encoding="utf-8") as file:
                self.wfile.write(bytes(file.read(), "utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            error_msg = f"<h3>Ошибка 404: Файл '{html_filename}' не найден в папке проекта!</h3>"
            self.wfile.write(bytes(error_msg, "utf-8"))

    # 3. ИСПРАВЛЕННЫЙ МЕТОД ОБРАБОТКИ ОТПРАВКИ ФОРМЫ
    def do_POST(self):
        if self.path == "/submit-contacts":
            # Определяем длину входящих данных формы
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            # Парсим полученные данные формы в словарь
            parsed_data = parse_qs(post_data)

            # ГАРАНТИРОВАННЫЙ ПЕРЕХВАТ: Получаем данные по id/name или берем первые попавшиеся ключи
            user_name = parsed_data.get('name', parsed_data.get('username', ['Не указано']))[0]
            user_email = parsed_data.get('email', ['Не указано'])[0]
            user_message = parsed_data.get('message', ['Не указано'])[0]

            # ВЫВОД В КОНСОЛЬ ПАЙЧАРМ (Обязательно напечатается)
            print("\n" + "=" * 40)
            print(" УСПЕШНО ПОЛУЧЕНЫ ДАННЫЕ ИЗ ФОРМЫ:")
            print(f" Имя пользователя: {user_name}")
            print(f" Электронная почта: {user_email}")
            print(f" Текст сообщения: {user_message}")
            print("=" * 40 + "\n")

            # Отправляем ответ пользователю об успешной отправке
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

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
                    <h2 class="fw-normal mb-3">Спасибо, {user_name}!</h2>
                    <p class="text-secondary mb-4">Ваше сообщение успешно получено сервером.</p>
                    <a href="/21-2_home4.html" class="btn btn-primary px-4">Назад к контактам</a>
                </div>
            </body>
            </html>
            """
            self.wfile.write(bytes(success_html, "utf-8"))


def run(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MyWebServer)
    print(f"==================================================")
    print(f" Умный сервер успешно перезапущен!")
    print(f" Откройте в браузере: http://localhost:{port}")
    print(f"==================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")


if __name__ == "__main__":
    run()
