import os
from flask import Flask, render_template_string, request
import yt_dlp

app = Flask(__name__)

# Automatically locate the downloads folder right next to app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Modern, responsive, streaming-themed HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Media Extractor & MusicBee Bridge</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #121212 0%, #1e1e2f 100%);
            color: #ffffff;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 16px;
            width: 100%;
            max-width: 600px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            text-align: center;
        }
        h1 { font-size: 26px; margin-bottom: 10px; color: #ffffff; }
        p { color: #b3b3b3; margin-bottom: 30px; font-size: 14px; }
        .input-group { display: flex; gap: 10px; margin-bottom: 20px; }
        input[type="text"] {
            flex: 1; padding: 14px 16px; font-size: 15px; border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.2); background: rgba(0, 0, 0, 0.2);
            color: white; outline: none; transition: border-color 0.3s;
        }
        input[type="text"]:focus { border-color: #1db954; }
        button {
            padding: 14px 24px; font-size: 15px; font-weight: bold; background: #1db954;
            color: white; border: none; border-radius: 8px; cursor: pointer; transition: background 0.3s;
        }
        button:hover { background: #1ed760; }
        .alert { margin-top: 20px; padding: 12px; border-radius: 8px; font-size: 14px; }
        .alert.success { background: rgba(29, 185, 84, 0.2); border: 1px solid #1db954; color: #1ed760; }
        .alert.error { background: rgba(255, 75, 75, 0.2); border: 1px solid #ff4b4b; color: #ff6b6b; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎵 Media Extractor</h1>
        <p>Paste a YouTube or streaming link below to convert and download your track instantly.</p>
        
        <form method="POST">
            <div class="input-group">
                <input type="text" name="url" placeholder="Paste link here (e.g., https://youtu.be/...)" required autocomplete="off">
                <button type="submit">Download</button>
            </div>
        </form>

        {% if message %}
            <div class="alert {{ status }}">
                {{ message }}
            </div>
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
        ydl_opts = {
            'format': 'bv*+ba/b',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'cookiefile': os.path.join(BASE_DIR, 'cookies.txt'),
            'js_runtimes': {'node': {}},  # Correct dictionary syntax for yt-dlp
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            message = "Success! Audio downloaded, converted, and saved to downloads."
            status = "success"
        except Exception as e:
            message = f"Extraction failed: {str(e)}"
            status = "error"
            
    return render_template_string(HTML_TEMPLATE, message=message, status=status)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
