from backend import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)  # 调试模式，自动重启代码修改