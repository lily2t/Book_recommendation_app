"""
This application will help the user by recommending a book by taking the user's preferences.
The application will ask the user to provide their preferences then will check for most relevant(similar)
books from an api of the open library, then suggest the user with three books of most convenient. 
"""
# Import necessary libraries
import requests
"""
Here i will implement OOP(object oriented programming) concept of python to identify the actors of the application.
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
    #iterate through the books data
    for genre in genres:
        genre_books = fetch_books_by_genre(genre)
        
        for book_info in genre_books:
            title = book_info.get("title", "")
            author = book_info.get("authors", [{}])[0].get("name", "")
            genres = book_info.get("subjects", [])

            book = Book(title=, author, genres)

            books.appen(book)

    return books        


def fetch_books_by_genre(genre):
    # Load book data from a file or API
    url = f"http://openlibrary.org/subjects/{genre}.json"
    response = requests.get(url)
    if response.status.code ==200:
        data = response.json()
        return data
    else:
        print("Error accuored while fetching books by genre.")
        return None


def preprocess_books(books):
    # Preprocess the book data (cleaning, organizing, etc.)
    pass

# Recommendation algorithm


def recommend_books(user, books):
    # Implement the recommendation algorithm
    pass

# User interface


def get_user_preferences():
    # Collect user preferences (genres, authors, etc.) from the user
    genres = input("Enter you preferred genres: ").split(",")
    authors = input("Enter your preferred authors name: ").split(",")

    return genres, authors


def display_recommendations(recommendations):
    # Display the recommended books to the user
    pass

# Main program


def main():
    # Load books
    books = load_books()

    # Preprocess books
    preprocessed_books = preprocess_books(books)

    # Create user
    user = User("John")  # Replace with user input for the name if desired

    # Get user preferences
    user_preferences = get_user_preferences()
    for preference in user_preferences:
        user.add_preference(preference)

    # Generate book recommendations
    recommendations = recommend_books(user, preprocessed_books)

    # Display recommendations
    display_recommendations(recommendations)


# Entry point
if __name__ == '__main__':
    main()
