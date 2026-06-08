import json
import os
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.json')


def load_data():
    """从 JSON 文件读取游戏数据"""
    if not os.path.exists(DATA_FILE):
        return {
            "high_score": 0,
            "total_games": 0,
            "total_kills": 0,
            "kills_by_type": {"small": 0, "medium": 0, "boss": 0},
            "last_score": 0
        }
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_data(data):
    """保存游戏数据到 JSON 文件"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.route('/')
def index():
    """返回游戏主页"""
    return render_template('index.html')


@app.route('/api/data', methods=['GET'])
def get_data():
    """获取游戏数据（最高分、统计等）"""
    return jsonify(load_data())


@app.route('/api/save', methods=['POST'])
def save_game_data():
    """更新游戏数据（保存新成绩）"""
    data = load_data()
    new_data = request.json
    for key in ('high_score', 'total_games', 'total_kills', 'kills_by_type', 'last_score'):
        if key in new_data:
            data[key] = new_data[key]
    save_data(data)
    return jsonify({"success": True})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
