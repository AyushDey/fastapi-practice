from fastapi import FastAPI

app = FastAPI()

class Books:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

books = [
    Books(1, "The Great Gatsby", "F. Scott Fitzgerald", "A classic novel set in the Jazz Age.", 5),
    Books(2, "To Kill a Mockingbird", "Harper Lee", "A novel about racial injustice in the Deep South.", 5),
    Books(3, "1984", "George Orwell", "A dystopian novel about totalitarianism.", 4),
    Books(4, "Pride and Prejudice", "Jane Austen", "A romantic novel about manners and marriage.", 4),
    Books(5, "The Hobbit", "J.R.R. Tolkien", "An epic fantasy adventure set in Middle-earth.", 3),
    Books(6, "The Catcher in the Rye", "J.D. Salinger", "A novel about teenage rebellion and alienation.", 4)
]

@app.get('/books/')
async def get_all_books():
    return books


