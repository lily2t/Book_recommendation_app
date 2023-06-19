"""
This application will help the user by recommending a book by taking the user's 
preferences(i.e by asking for genres or authors). The application will ask the 
user to provide their preferences then will check for most relevant(similar)
books from an api of the open library, then suggest the user with three books of 
most convenient. 
"""
import requests
import webbrowser


class Book:
    def __init__(self, title, author, subjects, key):
        self.title = title
        self.author = author
        self.subjects = subjects
        self.key = key


class User:
    def __init__(self, name):
        self.name = name
        self.preferences = []

    def add_preference(self, preference):
        self.preferences.append(preference)


def fetch_books_by_genre(genre):
    url = f"https://openlibrary.org/subjects/{genre}.json?limit=5"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "works" in data:
            books = data["works"]
            return books
        else:
            print("Invalid genre books:", data)
    else:
        print("Error loading the API.")
    return None


def load_books(genres):
    books = []
    for genre in genres:
        genre_books = fetch_books_by_genre(genre)
        if isinstance(genre_books, list):
            for book_info in genre_books:
                if isinstance(book_info, dict):
                    title = book_info.get("title", "")
                    author_info = book_info.get("authors", [])
                    author = author_info[0].get("name", "") if author_info else ""
                    subjects = book_info.get("subject", [])
                    key = book_info.get("key", "")
                    book = Book(title, author, subjects, key)
                    books.append(book)
                else:
                    print("Invalid book information:", book_info)
        else:
            print("Invalid genre books:", genre_books)
    return books


def preprocess_books(books, user):
    filtered_books = []
    for book in books:
        if any(genre in book.subjects for genre in user.preferences):
            filtered_books.append(book)
    return filtered_books


def recommend_books(user, books):
    sorted_books = sorted(books, key=lambda x: len(x.subjects), reverse=True)
    recommendations = sorted_books[:3]
    return recommendations


def get_user_preferences():
    name = input("Enter your name: ")

    while True:
        genres = input("Enter your preferred genres (comma-separated): ").split(",")
        if genres:
            break
        else:
            print("Invalid input. Please enter at least one genre.")

    return name, genres


def display_recommendations(recommendations):
    print("Here are the books I recommend you:")
    for i, book in enumerate(recommendations, start=1):
        print(f"{i}. {book.title} by {book.author}")
        print("   Opening Open Library page...")
        webbrowser.open_new_tab(f"https://openlibrary.org{book.key}")


def main():
    name, genres = get_user_preferences()
    user = User(name)
    books = load_books(genres)
    for preference in genres:
        user.add_preference(preference)
    preprocessed_books = preprocess_books(books, user)
    recommendations = recommend_books(user, preprocessed_books)
    display_recommendations(recommendations)


if __name__ == "__main__":
    main()
