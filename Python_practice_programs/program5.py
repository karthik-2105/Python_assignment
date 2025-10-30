import urllib.request
import re

def strip_html_tags(html_content):
    """Remove HTML tags using regex."""
    clean_text = re.sub(r'<[^>]+>', '', html_content)
    return clean_text

def main():
    # Take URL input from user
    url = input("Enter URL: ")

    try:
        # Fetch the HTML content from the given URL
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')

        # Strip HTML tags
        text = strip_html_tags(html)
        print("\n--- Clean Text ---\n")
        print(text)

        # Save the clean text to a file
        with open("clean_text.txt", "w", encoding="utf-8") as file:
            file.write(text)

        print("\n✅ Text successfully saved to 'clean_text.txt'.")

    except Exception as e:
        print("Error fetching URL:", e)


if __name__ == "__main__":
    main()
