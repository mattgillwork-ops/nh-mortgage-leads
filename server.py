import http.server
import socketserver
import os
import json

PORT = 2525
DIRECTORY = "tru/Inbox/"

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        if data.get("event") == "new_email":
            email_content = data.get("email")
            if email_content:
                file_path = os.path.join(DIRECTORY, f"{email_content}.tru")
                with open(file_path, "w") as file:
                    file.write(email_content)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Email stored successfully")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid email content")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid event type")

if __name__ == "__main__":
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)
    handler_object = MyHttpRequestHandler
    with socketserver.TCPServer(("", PORT), handler_object) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()
