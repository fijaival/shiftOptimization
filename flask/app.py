from api import create_app
import ssl

if __name__ == '__main__':
    app = create_app()
    app.run()
