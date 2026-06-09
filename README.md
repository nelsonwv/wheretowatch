# WhereToWatch 🎬

WhereToWatch is a Streamlit web app that helps users find where movies and TV shows are available for subscription streaming in different countries.

The app uses the TMDb API to search for titles, retrieve streaming provider availability, and display results in a clean, user-friendly interface.

## Features

* Search for movies and TV shows by title
* Select a country to check streaming availability
* View top matching results with posters, year, and media type
* See available subscription streaming providers
* Check fallback countries when a title is not available locally
* Custom dark-themed Streamlit interface

## Tech Stack

* Python
* Streamlit
* TMDb API
* Requests
* HTML/CSS for custom styling

## How It Works

1. The user selects a country and searches for a movie or TV show.
2. The app queries TMDb's multi-search endpoint.
3. Search results are cleaned and displayed as selectable cards.
4. The selected title is used to fetch country-specific watch provider data.
5. Subscription streaming providers are displayed with logos and provider links.

## API

This project uses data from [The Movie Database (TMDb)](https://www.themoviedb.org/).

To run the app, you need a TMDb API key stored in Streamlit secrets:

```toml
TMDB_API_KEY = "your_api_key_here"
```

## Run Locally

```bash
pip install streamlit requests
streamlit run app.py
```

## Project Purpose

This project was built to practice API integration, data cleaning, user interface design, and Streamlit app development.

It demonstrates how external data can be retrieved, transformed, and presented in an interactive web application.

## Future Improvements

* Add more countries
* Add filtering by provider
* Include rental and purchase options
* Add direct TMDb links for each title
* Improve error handling and loading states
* Deploy the app publicly

## Author

Created by Waldean Nelson
GitHub: [github.com/nelsonwv](https://github.com/nelsonwv)
