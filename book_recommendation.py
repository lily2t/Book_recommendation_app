"""
This application will help the user by recommending a book by taking the user's 
preferences(i.e by asking for genres or authors). The application will ask the 
user to provide their preferences then will check for most relevant(similar)
books from an api of the open library, then suggest the user with three books of 
most convenient. 
"""
# Import necessary libraries
import requests

"""
Here i will implement OOP(object oriented programming) concept of python to 
identify the actors of the application.
"""


class Book:
    def __init__(self, title, author, genres):
        self.title = title
        self.author = author
        self.genres = genres


class User:
    def __init__(self, name):
        self.name = name
        self.preferences = []

    def add_preference(self, preference):
        self.preferences.append(preference)


# Load book data from a file or API
def load_books(genres, authors):
    books = []
    # iterate through the books data
    for genre in genres:
        genre_books = fetch_books_by_genre(genre)

        if isinstance(genre_books, list):
            # Iterate through the books in the genre
            for book_info in genre_books:
                if isinstance(book_info, dict):
                    title = book_info.get("title", "")
                    author = book_info.get("authors", [{}])[0].get("name", "")
                    genres = book_info.get("subjects", [])

                    book = Book(title, author, genres)
                    books.append(book)
                else:
                    print("Invalid book information:", book_info)
        else:
            print("Invalid genre books:", genre_books)

    return books


def fetch_books_by_genre(genre):
    # Load book data from a file or API
    url = f"http://openlibrary.org/subjects/{genre}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, dict) and "works" in data:
            books = data["works"]
            return books
        else:
            print("Invalid genre books:", data)
    else:
        print("Facing problems while loading the API.")
    return None


# here we clean and organize our data before any recommendation
def preprocess_books(books, user):
    # Preprocess the book data (cleaning, organizing, etc.)
    filtered_books = []

    for book in books:
        if any(genre in book.genres for genre in user.preferences):
            filtered_books.append(book)
    return filtered_books


# Here we recommend the user by using popularity based filtering.
def recommend_books(user, books):
    # Sort books by popularity
    sorted_books = sorted(books, key=lambda x: len(x.editions), reverse=True)

    # Select the top three books
    recommendations = sorted_books[:4]

    return recommendations


# User interface
def get_user_preferences():
    # Collect user preferences (genres, authors, etc.) from the user
    genres = input("Enter you preferred genres: ").split(",")
    authors = input("Enter your preferred authors name: ").split(",")

    return genres, authors


# here we display the recommended books to the user
def display_recommendations(recommendations):
    # Display the recommended books to the user
    print("Here are the books i recommend you: ")
    for i, book in enumerate(recommendations, start=1):
        print(f"{i}. {book.title} by {book.author}")


def main():
    name = input("Enter your name? ")

    # Create user
    user = User(name)

    genres, authors = get_user_preferences()
    books = load_books(genres, authors)

    # Preprocess books
    preprocessed_books = preprocess_books(books, user)

    # Get user preferences
    user_preferences = get_user_preferences()

    for preference in user_preferences:
        user.add_preference(preference)

    # Generate book recommendations
    recommendations = recommend_books(user, preprocessed_books)

    # Display recommendations
    display_recommendations(recommendations)


# Entry point
if __name__ == "__main__":
    main()
