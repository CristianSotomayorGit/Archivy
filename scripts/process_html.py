# Import necessary classes from BeautifulSoup
from bs4 import BeautifulSoup, Tag

# Define a function to extract sections from an HTML file
def extract_sections(html_raw, html_extracted):
    
    # Open the raw HTML file for reading
    with open(html_raw, 'r', encoding='utf-8') as file:
        # Parse the HTML file using BeautifulSoup
        soup = BeautifulSoup(file, 'html.parser')

    # Find all elements in the HTML file
    elements = soup.find_all()

    # Open a new file to write the extracted HTML
    with open(html_extracted, 'w', encoding='utf-8') as file:

        # Iterate over each element in the HTML
        for i, elem in enumerate(elements):

            char_num = 0

            # Check if the element is not a tuple and is a leaf Tag (no child elements)
            if not isinstance(elem, tuple):
                if isinstance(elem, Tag) and not elem.find():
                    # Check if the element has a 'name' attribute
                    if 'name' in elem.attrs:

                        elem_name = elem['name']

                        # Write closing and opening div tags with the element's name
                        file.write('</div>')
                        file.write('<div id="' + elem_name + '">')

                    # Check if the element has text and write it to the file
                    if len(elem.get_text()) != 0:
                        elem_text = elem.get_text()
                        file.write(elem_text + '\n')
        # Close the file (not necessary as 'with' statement handles it)
        file.close

# Define a function to add classes to the extracted HTML based on bookmarks
def add_classes(html_extracted, html_bookmarks, html_with_classes):
    # Open the extracted HTML file for reading
    with open(html_extracted, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser') 
        # Find all div elements
        contElements = soup.find_all('div')

        # Open the bookmarks HTML file for reading
        with open(html_bookmarks, 'r', encoding='utf-8') as fileA:
            soupA = BeautifulSoup(fileA, 'html.parser')
            # Find all bookmark links
            bookmarksA = soupA.find_all('a', class_='bookmark')

            # Loop through each bookmark
            for bookmark in bookmarksA:
                # Extract the bookmark ID
                bookmarkA = bookmark['href'].split('#')[-1]
                label = bookmark.text

                # Loop through each div element in the extracted HTML
                for element in contElements:
                    # Check if the element ID matches the bookmark ID
                    if 'id' in element.attrs:
                        if bookmarkA == element['id']:
                            # Add a class to the element based on the bookmark label
                            element['class'] = element.get('class', []) + [label]           
    
    # Write the modified HTML to a new file
    with open(html_with_classes, 'w', encoding='utf-8') as output_file:
        output_file.write(soup.prettify())
    

# Define the main function
def main():
    # Define file paths
    html_raw = '=content.html'
    html_extracted = 'content_extracted.html'
    html_bookmarks = 'bookmarks.html'
    html_with_classes = 'content_with_classes.html'

    # Call functions to process the HTML files
    extract_sections(html_raw, html_extracted)
    add_classes(html_extracted, html_bookmarks, html_with_classes)

if __name__ == "__main__":
    main()
