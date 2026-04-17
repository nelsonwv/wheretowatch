# ---------------------------
# 1. Imports
# ---------------------------

import requests
import streamlit as st


# ---------------------------
# 2. App configuration
# ---------------------------

st.set_page_config(
    page_title="WhereToWatch",
    page_icon="🎬",
    layout="wide",
)


# ---------------------------
# 3. Constants and settings
# ---------------------------

TMDB_API_KEY = st.secrets["TMDB_API_KEY"]
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
TMDB_LOGO_BASE_URL = "https://image.tmdb.org/t/p/w154"

APP_TITLE = "WhereToWatch"
APP_TAGLINE = "Find where movies and TV shows are streaming in your country."

COUNTRY_OPTIONS = {
    "Australia": "AU",
    "Canada": "CA",
    "France": "FR",
    "Germany": "DE",
    "India": "IN",
    "Netherlands": "NL",
    "Spain": "ES",
    "Sweden": "SE",
    "United Kingdom": "GB",
    "United States": "US",
}

COUNTRY_CODE_TO_NAME = {code: name for name, code in COUNTRY_OPTIONS.items()}
FALLBACK_COUNTRIES = ["US", "GB", "CA", "AU", "IN"]

PROVIDER_LINKS = {
    "Netflix": "https://www.netflix.com",
    "Max": "https://www.max.com",
    "HBO Max": "https://www.max.com",
    "Amazon Prime Video": "https://www.primevideo.com",
    "Prime Video": "https://www.primevideo.com",
    "Disney Plus": "https://www.disneyplus.com",
    "Disney+": "https://www.disneyplus.com",
    "Apple TV Plus": "https://tv.apple.com",
    "Apple TV+": "https://tv.apple.com",
    "Hulu": "https://www.hulu.com",
    "Paramount Plus": "https://www.paramountplus.com",
    "Paramount+": "https://www.paramountplus.com",
    "Peacock": "https://www.peacocktv.com",
    "Viaplay": "https://viaplay.se",
    "NOW": "https://www.nowtv.com",
    "NOW TV": "https://www.nowtv.com",
}


# ---------------------------
# 4. Custom styling
# ---------------------------

st.markdown(
    """
    <style>
        /* ---------------------------
           Global styling
        --------------------------- */
        .stApp {
            background:
                radial-gradient(circle at top, rgba(173, 140, 84, 0.12), transparent 22%),
                linear-gradient(180deg, #111111 0%, #151515 100%);
            color: #F4EDE1;
            font-family: "Inter", "Helvetica Neue", "Arial", sans-serif;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3, h4, h5, h6, p, label, div, span {
            color: #F4EDE1;
        }

        /* ---------------------------
           Header
        --------------------------- */
        .hero-wrap {
            text-align: center;
            padding-top: 1.3rem;
            padding-bottom: 1.5rem;
        }

        .hero-title {
            font-size: 4.4rem;
            font-weight: 800;
            line-height: 0.95;
            letter-spacing: -0.04em;
            margin-bottom: 0.8rem;
            color: #F7F0E5;
            text-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
        }

        .hero-subtitle {
            font-size: 1.04rem;
            color: #B8AA94;
            max-width: 640px;
            margin: 0 auto;
            line-height: 1.7;
        }

        .hero-rule {
            width: 110px;
            height: 2px;
            background: #AD8C54;
            margin: 1rem auto 0 auto;
            opacity: 0.95;
        }

        /* ---------------------------
           Layout wrappers
        --------------------------- */
        .search-shell {
            max-width: 930px;
            margin: 0 auto 1.3rem auto;
        }

        .results-shell {
            max-width: 930px;
            margin: 0 auto 1.2rem auto;
        }

        .section-card {
            background: rgba(28, 28, 28, 0.88);
            border: 1px solid rgba(244, 237, 225, 0.08);
            border-radius: 22px;
            padding: 1.25rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 14px 35px rgba(0, 0, 0, 0.22);
        }

        .results-heading {
            font-size: 0.98rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #B8AA94;
            margin-bottom: 0.95rem;
        }

        /* ---------------------------
           Search form
        --------------------------- */
        div[data-testid="stForm"] {
            border: none;
            padding: 0;
            background: transparent;
        }

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div {
            border-radius: 14px !important;
            background-color: #1C1C1C !important;
            border: 1px solid rgba(244, 237, 225, 0.12) !important;
            min-height: 52px;
        }

        div[data-baseweb="input"] input {
            color: #F4EDE1 !important;
        }

        div[data-baseweb="select"] span {
            color: #F4EDE1 !important;
        }

        div[data-testid="stFormSubmitButton"] > button {
            width: 100%;
            min-height: 52px;
            margin-top: 1.72rem;
            border-radius: 14px;
            border: none;
            background: #AD8C54;
            color: #111111;
            font-weight: 800;
            letter-spacing: 0.01em;
        }

        div[data-testid="stFormSubmitButton"] > button:hover {
            background: #C8A56A;
            color: #111111;
        }

        /* ---------------------------
           Mini result cards
        --------------------------- */
        .mini-card {
            display: flex;
            gap: 16px;
            align-items: center;
            background: #171717;
            border: 1px solid rgba(244, 237, 225, 0.08);
            border-radius: 18px;
            padding: 0.9rem;
            margin-bottom: 0.8rem;
        }

        .mini-card-poster {
            width: 78px;
            height: 110px;
            object-fit: cover;
            border-radius: 12px;
            flex-shrink: 0;
        }

        .mini-card-fallback {
            width: 78px;
            height: 110px;
            border-radius: 12px;
            background: #262626;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #8F8577;
            font-size: 0.78rem;
            text-align: center;
            flex-shrink: 0;
            padding: 0.5rem;
        }

        .mini-card-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: #F7F0E5;
            margin-bottom: 0.35rem;
            line-height: 1.25;
        }

        .mini-card-meta {
            font-size: 0.92rem;
            color: #B8AA94;
            margin-bottom: 0.45rem;
        }

        .mini-card-badge {
            display: inline-block;
            padding: 0.24rem 0.62rem;
            border-radius: 999px;
            background: #AD8C54;
            color: #111111;
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }

        /* ---------------------------
           Radio group
        --------------------------- */
        div[role="radiogroup"] {
            background: #151515;
            border: 1px solid rgba(244, 237, 225, 0.08);
            border-radius: 16px;
            padding: 0.7rem 0.85rem;
            margin-top: 0.8rem;
        }

        /* ---------------------------
           Main media card
        --------------------------- */
        .media-title {
            font-size: 2.5rem;
            font-weight: 800;
            line-height: 1.03;
            letter-spacing: -0.03em;
            margin-bottom: 0.85rem;
            color: #F7F0E5;
        }

        .meta-text {
            color: #B8AA94;
            font-size: 1rem;
            margin-bottom: 0.8rem;
        }

        .media-badge {
            display: inline-block;
            padding: 0.3rem 0.78rem;
            border-radius: 999px;
            background-color: #AD8C54;
            color: #111111;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.03em;
            margin-bottom: 1.25rem;
            text-transform: uppercase;
        }

        .availability-heading {
            color: #F7F0E5;
            font-size: 1.18rem;
            font-weight: 800;
            margin-bottom: 0.8rem;
            line-height: 1.4;
        }

        .availability-subheading {
            color: #B8AA94;
            font-size: 0.94rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-top: 1.35rem;
            margin-bottom: 0.65rem;
        }

        .country-mini-heading {
            color: #F7F0E5;
            font-size: 1rem;
            font-weight: 700;
            margin-top: 0.9rem;
            margin-bottom: 0.55rem;
        }

        /* ---------------------------
           Provider blocks
        --------------------------- */
        .provider-row {
            display: flex;
            flex-wrap: wrap;
            gap: 18px;
            margin-top: 0.4rem;
            margin-bottom: 0.8rem;
        }

        .provider-block {
            width: 126px;
            text-align: center;
        }

        .provider-logo {
            width: 92px;
            height: 92px;
            object-fit: cover;
            border-radius: 20px;
            display: block;
            margin: 0 auto;
            box-shadow: 0 12px 24px rgba(0,0,0,0.28);
            background: #222222;
        }

        .provider-logo-placeholder {
            width: 92px;
            height: 92px;
            background: #2B2B2B;
            border-radius: 20px;
            margin: 0 auto;
        }

        .provider-name {
            font-size: 0.84rem;
            color: #F4EDE1;
            margin-top: 8px;
            line-height: 1.25;
            word-wrap: break-word;
        }

        /* ---------------------------
           Poster fallback
        --------------------------- */
        .poster-fallback {
            height: 560px;
            background: #242424;
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #8F8577;
            text-align: center;
            padding: 1rem;
            border: 1px solid rgba(244, 237, 225, 0.08);
        }

        /* ---------------------------
           Streamlit alert cleanup
        --------------------------- */
        div[data-testid="stAlert"] {
            border-radius: 16px;
            background: #1A1A1A;
            color: #F4EDE1;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------
# 5. Helper functions
# ---------------------------

def normalize_provider_name(provider_name):
    """
    Normalizes provider names so similar variations map to one clean display name.
    """
    normalization_map = {
        "HBO Max": "Max",
        "Disney Plus": "Disney+",
        "Apple TV Plus": "Apple TV+",
        "Paramount Plus": "Paramount+",
        "Amazon Prime Video": "Prime Video",
    }
    return normalization_map.get(provider_name, provider_name)


def format_media_type(media_type):
    """
    Converts raw TMDb media type values into cleaner labels for display.
    """
    media_type_map = {
        "movie": "Movie",
        "tv": "TV Show",
    }
    return media_type_map.get(media_type, "Unknown")


def build_provider_link(provider_name, country_code):
    """
    Generates a clickable homepage link for known streaming providers.
    """
    normalized_name = normalize_provider_name(provider_name)
    return PROVIDER_LINKS.get(normalized_name)


def clean_search_results(results):
    """
    Standardizes TMDb multi-search results into a clean shared structure.
    """
    cleaned_results = []

    for item in results:
        media_type = item.get("media_type")

        if media_type not in ["movie", "tv"]:
            continue

        if media_type == "movie":
            title = item.get("title", "Unknown Title")
            date_value = item.get("release_date", "")
        else:
            title = item.get("name", "Unknown Title")
            date_value = item.get("first_air_date", "")

        year = date_value[:4] if date_value else "Unknown"

        cleaned_results.append(
            {
                "id": item.get("id"),
                "media_type": media_type,
                "title": title,
                "year": year,
                "poster_path": item.get("poster_path"),
            }
        )

    return cleaned_results[:5]


def build_result_label(result):
    """
    Builds the radio-button label for each search result.
    """
    return f"{result['title']} ({result['year']}) — {format_media_type(result['media_type'])}"


# ---------------------------
# 6. API functions
# ---------------------------

@st.cache_data(show_spinner=False)
def search_titles(query):
    """
    Searches TMDb for movies and TV shows matching the user's query.
    """
    url = f"{TMDB_BASE_URL}/search/multi"
    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "include_adult": False,
        "language": "en-US",
        "page": 1,
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()
    raw_results = data.get("results", [])

    return clean_search_results(raw_results)


@st.cache_data(show_spinner=False)
def get_watch_providers(media_type, tmdb_id):
    """
    Fetches country-based watch provider data for a selected movie or TV show.
    """
    url = f"{TMDB_BASE_URL}/{media_type}/{tmdb_id}/watch/providers"
    params = {
        "api_key": TMDB_API_KEY,
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()
    return data.get("results", {})


def extract_subscription_providers(provider_data, country_code):
    """
    Filters provider data to return only subscription-based streaming services.
    """
    country_data = provider_data.get(country_code, {})
    flatrate_providers = country_data.get("flatrate", [])

    cleaned_providers = []
    seen_names = set()

    for provider in flatrate_providers:
        raw_name = provider.get("provider_name", "Unknown Provider")
        normalized_name = normalize_provider_name(raw_name)

        if normalized_name in seen_names:
            continue

        seen_names.add(normalized_name)

        cleaned_providers.append(
            {
                "provider_name": normalized_name,
                "logo_path": provider.get("logo_path"),
                "link": build_provider_link(normalized_name, country_code),
            }
        )

    return cleaned_providers


def check_fallback_countries(provider_data, fallback_list, user_country):
    """
    Checks fallback countries to see where a title is available via subscription.
    """
    fallback_results = []

    for country_code in fallback_list:
        if country_code == user_country:
            continue

        providers = extract_subscription_providers(provider_data, country_code)

        if providers:
            fallback_results.append(
                {
                    "country_code": country_code,
                    "country_name": COUNTRY_CODE_TO_NAME.get(country_code, country_code),
                    "providers": providers,
                }
            )

    return fallback_results


# ---------------------------
# 7. Display functions
# ---------------------------

def render_provider_html(providers):
    """
    Renders providers as HTML blocks so they can sit neatly inside the info panel.
    """
    if not providers:
        return "<p>No subscription providers found.</p>"

    html = '<div class="provider-row">'

    for provider in providers:
        logo_path = provider.get("logo_path")
        provider_name = provider.get("provider_name", "Unknown Provider")
        provider_link = provider.get("link")

        if logo_path:
            logo_url = f"{TMDB_LOGO_BASE_URL}{logo_path}"
            logo_html = f'<img src="{logo_url}" alt="{provider_name}" class="provider-logo">'
        else:
            logo_html = '<div class="provider-logo-placeholder"></div>'

        name_html = f'<div class="provider-name">{provider_name}</div>'
        inner_html = f"{logo_html}{name_html}"

        if provider_link:
            block_html = (
                f'<div class="provider-block">'
                f'<a href="{provider_link}" target="_blank" style="text-decoration:none;">'
                f"{inner_html}"
                f"</a>"
                f"</div>"
            )
        else:
            block_html = (
                f'<div class="provider-block">'
                f"{inner_html}"
                f"</div>"
            )

        html += block_html

    html += "</div>"
    return html


def render_result_cards(results):
    """
    Displays top matches as vertical mini cards.
    """
    for result in results:
        poster_path = result.get("poster_path")

        if poster_path:
            poster_html = (
                f'<img src="{TMDB_IMAGE_BASE_URL}{poster_path}" '
                f'alt="{result["title"]}" class="mini-card-poster">'
            )
        else:
            poster_html = '<div class="mini-card-fallback">No poster</div>'

        card_html = f"""
        <div class="mini-card">
            {poster_html}
            <div>
                <div class="mini-card-title">{result["title"]}</div>
                <div class="mini-card-meta">{result["year"]}</div>
                <div class="mini-card-badge">{format_media_type(result["media_type"])}</div>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)


def display_selected_media_card(title_data, provider_data, user_country):
    """
    Displays the selected title in a two-column card:
    poster on the left, streaming availability on the right.
    """
    user_country_name = COUNTRY_CODE_TO_NAME.get(user_country, user_country)
    user_providers = extract_subscription_providers(provider_data, user_country)
    fallback_results = check_fallback_countries(provider_data, FALLBACK_COUNTRIES, user_country)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    left_col, right_col = st.columns([1, 1.25], gap="large")

    with left_col:
        poster_path = title_data.get("poster_path")
        if poster_path:
            poster_url = f"{TMDB_IMAGE_BASE_URL}{poster_path}"
            st.image(poster_url, use_container_width=True)
        else:
            st.markdown(
                '<div class="poster-fallback">No poster available</div>',
                unsafe_allow_html=True,
            )

    with right_col:
        st.markdown(
            f'<div class="media-title">{title_data["title"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="meta-text">Year: {title_data["year"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="media-badge">{format_media_type(title_data["media_type"])}</div>',
            unsafe_allow_html=True,
        )

        if user_providers:
            st.markdown(
                f'<div class="availability-heading">Available in {user_country_name} on:</div>',
                unsafe_allow_html=True,
            )
            st.markdown(render_provider_html(user_providers), unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="availability-heading">Not currently available for subscription streaming in {user_country_name}.</div>',
                unsafe_allow_html=True,
            )

            if fallback_results:
                st.markdown(
                    '<div class="availability-subheading">Available for subscription streaming in:</div>',
                    unsafe_allow_html=True,
                )

                for country_result in fallback_results:
                    st.markdown(
                        f'<div class="country-mini-heading">{country_result["country_name"]}</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        render_provider_html(country_result["providers"]),
                        unsafe_allow_html=True,
                    )
            else:
                st.info(
                    "We couldn’t find streaming availability for this title. Try another title or check spelling."
                )

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------
# 8. Session state setup
# ---------------------------

if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "selected_result_index" not in st.session_state:
    st.session_state.selected_result_index = 0

if "last_query" not in st.session_state:
    st.session_state.last_query = ""


# ---------------------------
# 9. Header
# ---------------------------

st.markdown(
    f"""
    <div class="hero-wrap">
        <div class="hero-title">{APP_TITLE}</div>
        <div class="hero-subtitle">{APP_TAGLINE}</div>
        <div class="hero-rule"></div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------
# 10. Search section
# ---------------------------

st.markdown('<div class="search-shell">', unsafe_allow_html=True)
st.markdown('<div class="section-card">', unsafe_allow_html=True)

with st.form("search_form"):
    col1, col2, col3 = st.columns([1.05, 2.35, 0.8])

    with col1:
        country_name = st.selectbox(
            "Country",
            options=list(COUNTRY_OPTIONS.keys()),
            index=list(COUNTRY_OPTIONS.keys()).index("Sweden"),
        )

    with col2:
        title_query = st.text_input("Search title")

    with col3:
        search_clicked = st.form_submit_button("Search")

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

user_country_code = COUNTRY_OPTIONS[country_name]


# ---------------------------
# 11. Search logic
# ---------------------------

if search_clicked:
    st.session_state.selected_result_index = 0

    if not title_query.strip():
        st.session_state.search_results = []
        st.warning("Please enter a title before searching.")
    else:
        st.session_state.last_query = title_query.strip()

        with st.spinner("Searching titles..."):
            try:
                results = search_titles(title_query.strip())
                st.session_state.search_results = results

                if not results:
                    st.info(
                        "We couldn’t find streaming availability for this title. Try another title or check spelling."
                    )

            except requests.exceptions.RequestException:
                st.session_state.search_results = []
                st.error("Something went wrong while searching. Please try again.")


# ---------------------------
# 12. Match selection section
# ---------------------------

if st.session_state.search_results:
    st.markdown('<div class="results-shell">', unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="results-heading">Choose the correct title</div>',
        unsafe_allow_html=True,
    )

    render_result_cards(st.session_state.search_results)

    labels = [build_result_label(result) for result in st.session_state.search_results]

    selected_label = st.radio(
        "Top matches",
        options=labels,
        index=st.session_state.selected_result_index,
        label_visibility="collapsed",
    )

    selected_index = labels.index(selected_label)
    st.session_state.selected_result_index = selected_index
    selected_title = st.session_state.search_results[selected_index]

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------
    # 13. Selected title card + availability
    # ---------------------------

    with st.spinner("Checking streaming availability..."):
        try:
            provider_data = get_watch_providers(
                selected_title["media_type"],
                selected_title["id"],
            )
            display_selected_media_card(selected_title, provider_data, user_country_code)

        except requests.exceptions.RequestException:
            st.error("Something went wrong while checking streaming availability. Please try again.")