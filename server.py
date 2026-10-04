from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from urllib.parse import parse_qs


class MyWebServer(BaseHTTPRequestHandler):

    def do_GET(self):
        # 1. Если кликнули просто на корень http://localhost:8000/, открываем главную
        if self.path == "/":
            html_filename = "21-2_home1.html"

        # 2. Иначе убираем косую черту из пути (например, "/21-2_home4.html" превращаем в "21-2_home4.html")
        else:
            # Отрезаем параметры кэша, если они есть (все, что после знака вопроса)
            clean_path = self.path.split('?')[0]
            html_filename = clean_path.lstrip("/")

        # 3. Проверяем, существует ли такой HTML-файл в нашей папке
        if os.path.exists(html_filename) and html_filename.endswith(".html"):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            with open(html_filename, "r", encoding="utf-8") as file:
                self.wfile.write(bytes(file.read(), "utf-8"))

        # 4. Если файла в папке нет, показываем красивую ошибку 404
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            error_msg = f"<h3>Ошибка 404: Файл '{html_filename}' не найден в папке проекта!</h3>"
            self.wfile.write(bytes(error_msg, "utf-8"))

    # Обработка отправки формы из Контактов (остается без изменений)
    def do_POST(self):
        if self.path == "/submit-contacts":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            parsed_data = parse_qs(post_data)
            user_name = parsed_data.get('name', [''])[0]

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            success_html = f"""
            <!DOCTYPE html>
            <html lang="ru">
            <head><meta charset="UTF-8"><title>Успешно</title><link href="https://jsdelivr.net" rel="stylesheet"></head>
            <body class="bg-light d-flex align-items-center justify-content-center" style="height: 100vh;">
                <div class="card p-5 shadow-sm text-center">
                    <h2 class="text-success mb-3">✓ {user_name}, спасибо!</h2>
                    <p class="text-secondary mb-4">Ваше сообщение успешно отправлено.</p>
                    <a href="21-2_home4.html" class="btn btn-primary">Назад</a>
                </div>
            </body>
            </html>
            """
            self.wfile.write(bytes(success_html, "utf-8"))


def run(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MyWebServer)
    print(f"Умный сервер запущен на http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")


if __name__ == "__main__":
    run()
