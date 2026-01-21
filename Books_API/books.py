from fastapi import Body, FastAPI

app = FastAPI()

books = [
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "category": "Fiction"},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "category": "Fiction"},
    {"title": "1984", "author": "George Orwell", "category": "Science Fiction"},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "category": "Romance"},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "category": "Fantasy"}
]

# Path Parameter
@app.get("/books")
async def read_books():
    return books

# Query Parameter
@app.get("/books/")
async def get_category(category: str):
    category_books = []
    for book in books:
        if book.get('category').casefold() == category.casefold():
            category_books.append(book)
    return category_books

# Dynamic Parameter
@app.get("/books/{title}")
async def get_book(title: str):
    for book in books:
        if book['title'].casefold() == title.casefold():
            return book
        

# Post Request
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    books.append(new_book)

@app.put('/books/update_book')
async def update_book(updated_book=Body()):
    for i in range(len(books)):
        if books[i].get('title').casefold() == updated_book.get('title').casefold():
            books[i] = updated_book

@app.delete('/books/delete_book')
async def delete_book(book_name: str):
    for book in books:
        if book['title'].casefold() == book_name.casefold():
            books.remove(book)
            break

