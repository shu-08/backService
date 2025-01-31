from flask import Flask, render_template, request
from flask_cors import CORS  # flask_corsをインポート

import yt_dlp
import os

app = Flask(__name__)

# CORSを有効にする（特定のオリジンのみ許可）
CORS(app, resources={r"/*": {"origins": "https://front-service.vercel.app"}})

DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(url, download=True)
            file_path = os.path.join(DOWNLOAD_FOLDER, f"{video_info['title']}.{video_info['ext']}")
        
        return render_template('index.html', download_link=file_path)
    
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
