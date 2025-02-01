from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)

CORS(app, origins="https://front-service.vercel.app")

DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return "API is working!"

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    urls = data.get('urls', [])  # リストとして受け取る

    if not urls:
        return jsonify({'error': 'URLが指定されていません'}), 400

    download_links = []

    for url in urls:
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                video_info = ydl.extract_info(url, download=True)
                file_name = f"{video_info['title']}.{video_info['ext']}"
                file_path = os.path.join(DOWNLOAD_FOLDER, file_name)

            # 公開用のリンク（本番環境では適切なURLを指定する）
            download_links.append(f"https://backservice-oqui.onrender.com/download_file/{file_name}")

        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return jsonify({'download_links': download_links})

@app.route('/download_file/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'ファイルが見つかりません'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
