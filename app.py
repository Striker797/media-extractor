import os
from flask import Flask, request, render_template_string
import yt_dlp

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Media Extractor</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #121212;
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .card {
            background-color: #1e1e1e;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            width: 100%;
            max-width: 400px;
            box-sizing: border-box;
            text-align: center;
        }
        h2 { margin-bottom: 10px; color: #b19cd9; }
        p { color: #aaaaaa; font-size: 14px; margin-bottom: 20px; }
        input[type="text"] {
            width: 100%;
            padding: 12px;
            border: 1px solid #333;
            border-radius: 6px;
            background-color: #2a2a2a;
            color: #fff;
            font-size: 14px;
            margin-bottom: 15px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 6px;
            background-color: #22c55e;
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }
        button:hover { background-color: #16a34a; }
        .alert {
            margin-top: 15px;
            padding: 10px;
            border-radius: 6px;
            font-size: 13px;
        }
        .alert.success { background-color: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid #22c55e; }
        .alert.error { background-color: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #ef4444; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🎵 Media Extractor</h2>
        <p>Paste a YouTube or streaming link below to convert and download your track instantly.</p>
        <form method="POST">
            <input type="text" name="url" placeholder="Paste link here (e.g., https://...)" required>
            <button type="submit">Download</button>
        </form>
        {% if message %}
            <div class="alert {{ status }}">{{ message }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    status = ""
    if request.method == "POST":
        url = request.form.get("url")
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'cookiefile': 'cookies.txt',
                'js_runtimes': {'node': {}}, 
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            message = "Success! Audio downloaded, converted, and saved."
            status = "success"
        except Exception as e:
            message = f"Extraction failed: {str(e)}"
            status = "error"

    return render_template_string(HTML_TEMPLATE, message=message, status=status)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
