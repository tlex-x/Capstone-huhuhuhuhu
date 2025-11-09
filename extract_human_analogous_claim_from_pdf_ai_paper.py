import fitz  # PyMuPDF
import re
import os

# Commented out IPython magic to ensure Python compatibility.
# %pip install PyMuPDF pandas

from google.colab import files

uploaded = files.upload()
file_name = next(iter(uploaded))

"""Convert pdf => txt file"""

try:
    with fitz.open(file_name) as doc:
        text = ""
        for page in doc:
            text += page.get_text()

    # Define the output text file name
    output_text_file = file_name.replace('.pdf', '.txt') if file_name.endswith('.pdf') else file_name + '.txt'

    # Write the extracted text to a .txt file
    with open(output_text_file, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Successfully converted '{file_name}' to '{output_text_file}'")
    print(f"Content of '{output_text_file}':")
    print(text[:500] + "..." if len(text) > 500 else text) # Displaying first 500 characters

except FileNotFoundError:
    print(f"Error: File '{file_name}' not found. Please upload the PDF file first.")
except Exception as e:
    print(f"An error occurred: {e}")

"""Delete line break, any "-"
"""

try:
    # Read the content of the text file
    with open(output_text_file, "r", encoding="utf-8") as f:
        text_content = f.read()

    # Remove "- " followed by any type of line break (\r\n, \n, or \r)
    text_without_specific_linebreaks = re.sub(r'- *\r?\n', '', text_content)
    text_without_specific_linebreaks = re.sub(r'- *\r', '', text_without_specific_linebreaks) # Handle cases with only \r
    text_without_specific_linebreaks = text_without_specific_linebreaks.replace('\n', ' ').replace('\r', ' ')

    # Overwrite the original text file with the modified content
    with open(output_text_file, "w", encoding="utf-8") as f:
        f.write(text_without_specific_linebreaks)

    print(f"Successfully removed '- ' followed by line breaks from '{output_text_file}'.")
    print(f"Content of '{output_text_file}' after removing specific line breaks:")
    print(text_without_specific_linebreaks[:500] + "..." if len(text_without_specific_linebreaks) > 500 else text_without_specific_linebreaks) # Displaying first 500 characters

except FileNotFoundError:
    print(f"Error: File '{output_text_file}' not found. Please ensure the PDF was converted to text first.")
except Exception as e:
    print(f"An error occurred: {e}")

"""remove pre abstract & post reference"""

try:
    # Read the content of the text file
    with open(output_text_file, "r", encoding="utf-8") as f:
        text_content = f.read()

    # Find the index of the word "abstract" (case-insensitive)
    abstract_index = re.search(r'\babstract\b', text_content, re.IGNORECASE)

    # Find the index of the word "references" (case-insensitive)
    references_index = re.search(r'\breferences\b', text_content, re.IGNORECASE)

    modified_text = text_content

    if abstract_index:
        # Truncate the text content from the beginning up to the word "abstract"
        modified_text = modified_text[abstract_index.start():]
    else:
        print(f"The word 'abstract' was not found in '{output_text_file}'. Content before it was not removed.")

    if references_index:
        # Truncate the text content at the beginning of the word "references"
        # We need to adjust the index based on whether content before "abstract" was removed
        if abstract_index and references_index.start() > abstract_index.start():
             adjusted_references_index = references_index.start() - abstract_index.start()
             modified_text = modified_text[:adjusted_references_index]
        elif not abstract_index:
             modified_text = modified_text[:references_index.start()]
        else:
             print(f"The word 'references' was found before 'abstract'. Content after it was not removed in the intended way.")
    else:
        print(f"The word 'references' was not found in '{output_text_file}'. Content after it was not removed.")


    # Overwrite the original text file with the modified content
    with open(output_text_file, "w", encoding="utf-8") as f:
        f.write(modified_text)

    print(f"Successfully modified '{output_text_file}' by removing content before 'abstract' and after 'references'.")
    print(f"Content of '{output_text_file}' after modification:")
    print(modified_text[:500] + "..." if len(modified_text) > 500 else modified_text) # Displaying first 500 characters

except FileNotFoundError:
    print(f"Error: File '{output_text_file}' not found. Please ensure the PDF was converted to text first.")
except Exception as e:
    print(f"An error occurred: {e}")

"""Each sentence occupy a line"""

try:
    # Read the content of the text file
    with open(output_text_file, "r", encoding="utf-8") as f:
        text_content = f.read()

    # Split the text into sentences. Modified regex to avoid splitting after "et al."
    # This regex splits after a period, question mark, or exclamation point followed by a space,
    # but avoids splitting on common abbreviations, decimal points, and "et al."
    sentences = re.split(r'(?<!et al\.)(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s', text_content)

    # Join the sentences back together with a newline after each one
    text_with_linebreaks = "\n".join(sentences)

    # Overwrite the original text file with the modified content
    with open(output_text_file, "w", encoding="utf-8") as f:
        f.write(text_with_linebreaks)

    print(f"Successfully added line breaks after each sentence in '{output_text_file}'.")
    print(f"Content of '{output_text_file}' after adding line breaks:")
    print(text_with_linebreaks[:500] + "..." if len(text_with_linebreaks) > 500 else text_with_linebreaks) # Displaying first 500 characters

except FileNotFoundError:
    print(f"Error: File '{output_text_file}' not found. Please ensure the text file was created and modified in previous steps.")
except Exception as e:
    print(f"An error occurred: {e}")

"""count for learn and understand"""

import re
import os

# Assuming the text file has line breaks after each sentence from previous steps
# You might need to adjust the file name if it's different
output_text_file = file_name.replace('.pdf', '.txt') if file_name.endswith('.pdf') else file_name + '.txt'

try:
    learn_lines = []
    understand_lines = []
    learn_line_count = 0
    understand_line_count = 0

    with open(output_text_file, "r", encoding="utf-8") as f:
        for line in f:
            line_lower = line.lower()
            if "learn" in line_lower:
                learn_line_count += 1
                learn_lines.append(line.strip())
            if "understand" in line_lower:
                understand_line_count += 1
                understand_lines.append(line.strip())

    print(f"Number of lines containing 'learn': {learn_line_count}")
    print(f"Number of lines containing 'understand': {understand_line_count}")

    print("\nLines containing 'learn':")
    if learn_lines:
        for i, line in enumerate(learn_lines):
            print(f"{i+1}. {line}")
    else:
        print("No lines found containing 'learn'.")

    print("\nLines containing 'understand':")
    if understand_lines:
        for i, line in enumerate(understand_lines):
            print(f"{i+1}. {line}")
    else:
        print("No lines found containing 'understand'.")

except FileNotFoundError:
    print(f"Error: File '{output_text_file}' not found. Please ensure the text file was created and modified in previous steps.")
except Exception as e:
    print(f"An error occurred: {e}")
