from playwright.async_api import (
    Playwright, async_playwright,
)
from playwright._impl._api_types import (
    TimeoutError as PWTimeOutErr,
)
import asyncio
from pathlib import Path
import re
from rich.console import Console
from rich import print as richprint
import random

import json
import csv


DUOLINGO_WORDS_URL = "https://duome.eu/vocabulary/en/ja"

FILENAME = DUOLINGO_WORDS_URL.replace("https://duome.eu/vocabulary/", "").replace("/", "_")


# [
#   ['original_word', 'html_original_word', 'html_definition', 'category', 'html_category'],
#   [...]
# ]

async def pw_duome_scraper(playwright: Playwright) -> None:

    '''
    Scrapes the duome website's words, prettifies them using function `prettifier_for_anki` and stores them into the global variable `LIST_WHOLE_WORDS`.

    ### Parameters
        `playwright (Playwright)`: Takes the playwright's class to open the browser asynchronously.
    '''

    global FOUND_LANGS

    # Get the path of the current script file (running Python)
    current_script_path = Path(__file__).resolve()
    # Use the resolved path to access the file or its parent directory
    resolve_persistent_dir = current_script_path.parent / "PersistentContext"

    browser_type = playwright.chromium
    browser = await browser_type.launch_persistent_context(
        user_data_dir=str(resolve_persistent_dir),
        headless=False,
        channel="msedge",
        #slow_mo=10,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57",
        args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage",
            "--disable-component-extensions-with-background-pages",
        ],
        # Set locale & timezone so websites always load in English
        locale="en-US",
        timezone_id="Europe/London"
    )

    page = await browser.new_page()

    # Set viewport size like a fake laptop
    await page.set_viewport_size({"width": 1244, "height": 830})

    # Extract language codes from the URL
    # Define the regex pattern to extract language codes
    extract_langcode_from_url_pattern = r"https://duome\.eu/vocabulary/([a-z]{2})/([a-z]{2})"

    # Use regular expression to extract language codes
    lang_code_matches = re.search(
        pattern=extract_langcode_from_url_pattern,
        string=DUOLINGO_WORDS_URL
    )
    language_codes_list = [lang.upper() for lang in lang_code_matches.groups()]
    
    FOUND_LANGS = language_codes_list

    await page.goto(
        url=DUOLINGO_WORDS_URL,
        wait_until="load",
        # Timeout: 3 minutes
        timeout=180000,
    )

    #* Get total available words count
    #? document.querySelector("small[class='cCCC']").textContent
    total_words_element = await page.query_selector(
        selector="small[class='cCCC']"
    )
    total_words_text = str(await total_words_element.text_content())
    total_words = int(
        re.search(
            pattern=r"\b\d+\b",
            string=total_words_text,
        ).group()
    )

    #* Get a list of all words (li elements), exclude header alphabets that have class='single' 
    #? document.querySelectorAll("div[id='words'] li:not(.single)")
    # or: const word_element = document.querySelectorAll("div[id='words'] li:not(.single)")[0];

    all_visible_words_element = await page.query_selector_all(
        selector="div[id='words'] li:not(.single)",
    )
    # Colorize the final word count
    if len(all_visible_words_element) == total_words:
        colorized_word_count_result = "green"
    elif len(all_visible_words_element) < total_words:
        # FFC411 = orange
        colorized_word_count_result = "#FFC411"
    richprint(
        f"[bold]Total Words Found: [{colorized_word_count_result}]{len(all_visible_words_element)}[/{colorized_word_count_result}]/[green]{total_words}[/green][/bold] (Visible Words Elements/Total Words)"
    )

    rich_console = Console()

    # Iterate through elements & access their attributes|content
    for i, word_element in enumerate(all_visible_words_element):

        """ if i == 100:
            break """

        # end="\r" to print on same line as before (no print on newline, updating current line)
        rich_console.print(f"[bold][red]   Scarping Words:[/red] [#C5FF33]{i + 1}[/#C5FF33]/[green]{total_words}[/green][/bold]", end="\r")
        
        # List of current word (word, definition, category)

        #* Access original word
        #? word_element.querySelector("span[class='hide wN']").textContent
        original_word_element = await word_element.query_selector(
            selector="span[class='hide wN']"
        )
        original_word = str(await original_word_element.text_content())
        #* Access original word with phonetic symbols (e.g. ò)
        #? word_element.querySelector("span[class='speak xs voice']").textContent
        original_phoneticword_element = await word_element.query_selector(
            selector="span[class='speak xs voice']"
        )
        original_phoneticword = str(await original_phoneticword_element.text_content())

        #* Access definition (displayed on hover on the word)
        #? word_element.querySelector("span[class='wA']").getAttribute("title")
        word_definition_element = await word_element.query_selector(
            selector="span[class='wA']"
        )
        word_definition = str(
            await word_definition_element.get_attribute(
                name="title"
            )
        )
        #* Remove the [original_word] from the definition, only from the beginnig of the string
        word_definition = re.sub(
            # Remove the [original_word] and any whitespace after it
            pattern=rf"\[{original_word}\]\s*",
            repl="",
            string=word_definition,
            # Only from the beginning of the text
            count=1,
        )

        #* Access word category (part of speech), like: Adverb, must remove "·  " from the string
        #? word_element.querySelector("small[class='cCCC wP']").textContent
        word_category_element = await word_element.query_selector(
            selector="small[class='cCCC wP']"
        )
        word_category_text = str(await word_category_element.text_content())
        #* Remove the dot and any number of whitespaces it have, only from the beginning of the string
        word_category = re.sub(
            # Remove the dot and any number of whitespaces it have
            pattern=r"·\s*",
            repl="",
            string=word_category_text,
            # Only from the beginning of the text
            count=1,
        )

        append_to_csv([original_phoneticword, word_definition, word_category], f'{FILENAME}_{total_words}.csv')

def append_to_csv(input_data, filename):
    """Appends the `input_data` list as a new row in the specified `filename`.
    
    Args:
        input_data (list): A list of values to be added as a new row.
                           Each element corresponds to a column value.
        filename (str): The path to the target CSV file.
    """

    # Open the file in append mode ('a'), specifying utf-8 encoding
    with open(filename, 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write the `input_data` as a new row
        writer.writerow(input_data)

async def main():

    '''
    Runs the functions that have `Playwright` as parameter, then runs other necessary functions after closing the browser.
    '''

    async with async_playwright() as playwright:

        await pw_duome_scraper(
            playwright=playwright
        )

# Run the async function
asyncio.run(
    main()
)