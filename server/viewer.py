from basic_db import db, Text

def print_all_texts():
    with app.app_context():
        texts = Text.query.all()
        for text in texts:
            print(text.content)

if __name__ == "__main__":
    print_all_texts()
