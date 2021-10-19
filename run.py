from rabbitai import create_app

if __name__ == '__main__':
    rabbitai_app = create_app()

    rabbitai_app.run(host="127.0.0.1", port="8088", debug=True)

