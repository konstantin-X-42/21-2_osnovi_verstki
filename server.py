from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse


class MyWebServer(BaseHTTPRequestHandler):

    def do_GET(self):
        # ЗАДАНИЕ 2: На ЛЮБОЙ GET-запрос возвращаем страницу «Контакты»
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

        # Содержимое для отправки читаем из HTML-файла через with open()
        filename = '21-2_home4.html'
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            self.wfile.write(bytes(content, 'utf-8'))

    def do_POST(self):
        # Обработка POST-запроса от формы
        if self.path == '/submit-contacts':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            parsed_data = urllib.parse.parse_qs(post_data)

            print("\n--- Получены данные из формы Контакты ---")
            print(f"Имя: {parsed_data.get('name', [''])}")
            print(f"Почта: {parsed_data.get('email', [''])}")
            print(f"Сообщение: {parsed_data.get('message', [''])}")
            print("-------------------------------------------\n")

            # Перенаправляем обратно на контакты
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()


def run(server_class=HTTPServer, handler_class=MyWebServer):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print("Сервер запущен на http://localhost:8000/")
    httpd.serve_forever()


if __name__ == '__main__':
    run()

# from http.server import HTTPServer, BaseHTTPRequestHandler
# import urllib.parse
# import os
#
#
# class MyWebServer(BaseHTTPRequestHandler):
#
#     def do_GET(self):
#         # 1. ОБРАБОТКА СТИЛЕЙ (Исправляет ошибку 404 для CSS-файлов)
#         if self.path == '/style.css' or self.path == '/css/bootstrap.min.css':
#             # Убираем начальный слэш, чтобы получить корректный локальный путь к файлу
#             local_path = self.path.lstrip('/')
#
#             if os.path.exists(local_path):
#                 self.send_response(200)
#                 self.send_header('Content-Type', 'text/css; charset=utf-8')
#                 self.end_headers()
#                 # Читаем стили с помощью контекстного менеджера
#                 with open(local_path, 'r', encoding='utf-8') as f:
#                     self.wfile.write(bytes(f.read(), 'utf-8'))
#                 return
#             else:
#                 self.send_error(404, f"CSS File Not Found: {local_path}")
#                 return
#
#         # 2. МАРШРУТИЗАЦИЯ HTML СТРАНИЦ
#         if self.path == '/' or self.path == '/21-2_home1.html':
#             filename = '21-2_home1.html'
#         elif self.path == '/21-2_home2.html':
#             filename = '21-2_home2.html'
#         elif self.path == '/21-2_home3.html':
#             filename = '21-2_home3.html'
#         elif self.path == '/21-2_home4.html':
#             filename = '21-2_home4.html'
#         else:
#             # Реализация дополнительного функционала: страница 404 (Критерий №4)
#             self.send_response(404)
#             self.send_header('Content-Type', 'text/html; charset=utf-8')
#             self.end_headers()
#             self.wfile.write(b"<h1>404 Not Found</h1><p>Izvinite, takoy stranici net.</p>")
#             return
#
#         # Успешный ответ HTML (Критерий №5)
#         try:
#             self.send_response(200)
#             self.send_header('Content-Type', 'text/html; charset=utf-8')
#             self.end_headers()
#
#             # Чтение файла с помощью контекстного менеджера (Критерий №6)
#             with open(filename, 'r', encoding='utf-8') as f:
#                 content = f.read()
#                 self.wfile.write(bytes(content, 'utf-8'))
#         except FileNotFoundError:
#             self.send_error(500, "Internal Server Error: File not found")
#
#     def do_POST(self):
#         # Сервер принимает POST-запрос (Критерий №7)
#         if self.path == '/submit-contacts':
#             content_length = int(self.headers['Content-Length'])
#             post_data = self.rfile.read(content_length).decode('utf-8')
#
#             # Парсим полученные из формы данные
#             parsed_data = urllib.parse.parse_qs(post_data)
#
#             # Выводим данные в консоль без ошибок (Критерий №7)
#             print("\n--- Получены данные из формы Контакты ---")
#             print(f"Имя: {parsed_data.get('name', [''])[0]}")
#             print(f"Почта: {parsed_data.get('email', [''])[0]}")
#             print(f"Сообщение: {parsed_data.get('message', [''])[0]}")
#             print("-------------------------------------------\n")
#
#             # Перенаправляем обратно на страницу контактов после отправки
#             self.send_response(303)
#             self.send_header('Location', '/21-2_home4.html')
#             self.end_headers()
#
#
# # Запуск сервера на порту 8000
# def run(server_class=HTTPServer, handler_class=MyWebServer):
#     server_address = ('', 8000)
#     httpd = server_class(server_address, handler_class)
#     print("Сервер запущен на http://localhost:8000/")
#     httpd.serve_forever()
#
#
# if __name__ == '__main__':
#     run()
