from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)

# CORS設定
CORS(app, origins="https://front-service.vercel.app")

# 動画の保存先
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return "API is working!"

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(url, download=True)
            # ダウンロードされたファイルのフルパスを生成
            file_path = os.path.join(DOWNLOAD_FOLDER, f"{video_info['title']}.{video_info['ext']}")
        
        return jsonify({'download_link': file_path}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
