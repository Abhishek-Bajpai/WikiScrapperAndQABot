import wikipedia

def get_linked_articles(article_title):
    # Get the Wikipedia page
    try:
        page = wikipedia.page(article_title)
    except wikipedia.exceptions.PageError:
        print(f"Error: Wikipedia page for '{article_title}' not found.")
        return [], []
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"Disambiguation error: {e}")
        return [], []

    # Extract links from the page
    links = page.links
    linked_articles = []
    dead_links = []

    # Iterate over each linked article and extract its content
    for link in links:
        try:
            linked_page = wikipedia.page(link)
            linked_articles.append((linked_page.title, linked_page.content))
        except wikipedia.exceptions.PageError:
            print(f"Error: Wikipedia page for '{link}' not found.")
            dead_links.append(link)
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"Disambiguation error: {e}")
            dead_links.append(link)
    
    return linked_articles, dead_links


def save_content_to_file(linked_articles, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for title, content in linked_articles:
            f.write(f"### {title}\n")
            f.write(content)
            f.write("\n\n")
    print(f"All linked articles saved to {output_file}")

def save_dead_links_to_file(dead_links, dead_links_file):
    with open(dead_links_file, "w") as f:
        for link in dead_links:
            f.write(link + "\n")
    print(f"All dead links saved to {dead_links_file}")

if __name__ == "__main__":
    # Specify the title of the Wikipedia article you want to read
    article_title = "Python (programming language)"

    # Specify the output files to save the content and dead links
    output_file = "linked_articles_content.txt"
    dead_links_file = "dead_links.txt"

    # Get linked articles and dead links
    linked_articles, dead_links = get_linked_articles(article_title)

    # Save content to file
    save_content_to_file(linked_articles, output_file)

    # Save dead links to file
    save_dead_links_to_file(dead_links, dead_links_file)
