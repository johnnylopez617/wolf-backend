from app import create_app
from dotenv import load_dotenv
import os

load_dotenv()

app = create_app(os.environ.get('FLASK_ENV', 'default'))

if __name__ == '__main__':
    app.run(debug=True)
