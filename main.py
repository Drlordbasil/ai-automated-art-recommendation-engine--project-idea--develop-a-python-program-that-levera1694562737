import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import random


class Artwork:
    def __init__(self, title, artist, genre, description):
        self.title = title
        self.artist = artist
        self.genre = genre
        self.description = description

    def display_details(self):
        print("Title:", self.title)
        print("Artist:", self.artist)
        print("Genre:", self.genre)
        print("Description:", self.description)


class ArtRecommender:
    def __init__(self):
        self.artwork_data = []
        self.artwork_vectors = None
        self.user_profiles = {}
        self.vectorizer = TfidfVectorizer()

    def scrape_artwork_data(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        artwork_titles = [
            title.text.strip() for title in soup.find_all("h2", class_="artwork-title")
        ]
        artwork_artists = [
            artist.text.strip()
            for artist in soup.find_all("h3", class_="artwork-artist")
        ]
        artwork_genres = [
            genre.text.strip() for genre in soup.find_all("a", class_="artwork-genre")
        ]
        artwork_descriptions = [
            description.text.strip()
            for description in soup.find_all("p", class_="artwork-description")
        ]

        for title, artist, genre, description in zip(
            artwork_titles, artwork_artists, artwork_genres, artwork_descriptions
        ):
            artwork = Artwork(title, artist, genre, description)
            self.artwork_data.append(artwork)

    def create_user_profile(self, username):
        preferences = input("Please enter your art preferences, separated by commas: ")
        self.user_profiles[username] = preferences.split(",")

    def generate_artwork_vectors(self):
        artwork_texts = [
            artwork.title + " " + artwork.description for artwork in self.artwork_data
        ]
        self.artwork_vectors = self.vectorizer.fit_transform(artwork_texts).todense()

    def recommend_artwork(self, username):
        if username not in self.user_profiles:
            print("User profile not found.")
            return

        user_preferences = self.user_profiles[username]

        user_vector = self.vectorizer.transform([" ".join(user_preferences)]).todense()

        similarity_scores = cosine_similarity(
            user_vector, self.artwork_vectors
        ).flatten()

        sorted_indices = np.argsort(similarity_scores)[::-1]

        recommended_indices = random.sample(
            sorted_indices.tolist(), min(5, len(sorted_indices))
        )

        print(f"Recommended artworks for {username}:")
        for index in recommended_indices:
            artwork = self.artwork_data[index]
            artwork.display_details()


if __name__ == "__main__":
    recommender = ArtRecommender()
    recommender.scrape_artwork_data("https://www.example.com/artworks")
    recommender.create_user_profile("JohnDoe")
    recommender.generate_artwork_vectors()
    recommender.recommend_artwork("JohnDoe")
