from flask import Flask, request, jsonify, send_file
from werkzeug.utils import safe_join
from flask_cors import CORS  # 追加
import yt_dlp
import os
import uuid

app = Flask(__name__)
CORS(app)  # すべてのリクエストを許可（本番環境では適切に設定）

DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return "API is working!"

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    print(f"受信したデータ: {data}")  # デバッグ用

    urls = data.get('urls', [])  
    if not urls:
        print("エラー: URLが指定されていません")
        return jsonify({'error': 'URLが指定されていません'}), 400

    download_links = []
    
    for url in urls:
        try:
            random_filename = uuid.uuid4().hex
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, f'{random_filename}.%(ext)s'),
            }
            
            print(f"ダウンロード開始: {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                video_info = ydl.extract_info(url, download=True)
                ext = video_info.get('ext', 'mp4')
                file_name = f"{random_filename}.{ext}"
                file_path = os.path.join(DOWNLOAD_FOLDER, file_name)

            if os.path.exists(file_path):
                download_link = f"https://backservice-oqui.onrender.com/download_file/{file_name}"
                download_links.append(download_link)
                print(f"ダウンロード成功: {download_link}")
            else:
                print(f"エラー: ファイルが見つかりません {file_name}")
                return jsonify({'error': f'ファイルが見つかりません: {file_name}'}), 400

        except Exception as e:
            print(f"エラー: {str(e)}")
            return jsonify({'error': str(e)}), 400

    return jsonify({'download_links': download_links})

@app.route('/download_file/<filename>', methods=['GET'])
def download_file(filename):
    file_path = safe_join(DOWNLOAD_FOLDER, filename)
    print(f"ダウンロードリクエスト: {file_path}")

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'ファイルが見つかりません'}), 404
