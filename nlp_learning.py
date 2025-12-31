import requests
import urllib3
from nltk import FreqDist
from nltk.corpus import stopwords

# Disable SSL warnings for office network compatibility
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def fetch_book_text(url):
    """Downloads the text from a URL and returns a string."""
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Failed to download book: {e}")
        return None


def process_words(text, remove_stops=True):
    """Splits text into words and optionally removes stop words."""
    words = text.split()

    if remove_stops:
        stop_words = set(stopwords.words('english'))
        # Using a list comprehension for efficiency
        words = [word for word in words if word.lower() not in stop_words]

    return words


def main():
    # 1. Configuration
    book_url = "https://www.gutenberg.org/files/16/16-0.txt"

    # 2. Execution
    raw_text = fetch_book_text(book_url)

    if raw_text:
        # Clean and filter the words
        filtered_words = process_words(raw_text, remove_stops=True)

        # Calculate frequency distribution
        word_freq = FreqDist(filtered_words)

        # 3. Output Results
        top_10 = word_freq.most_common(10)

        print("Top 10 Words (Cleaned):")
        print("-" * 25)
        for word, count in top_10:
            print(f"{word:12}: {count}")

        # Accessing the 1st most common frequency as requested
        print("-" * 25)
        top_word, top_count = word_freq.most_common(1)[0]

        print(f"Highest Frequency Word: {top_word} \n"
              f"Frequency: {top_count}")

if __name__ == "__main__":
    main()