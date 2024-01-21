# Duolingo Scraper
<center>
  <img src="https://i.postimg.cc/W14rPY3b/Duolingo-In-Love-With-Anki.png" width="200" height="150">
</center>

This project scrapes any languages available on Duolingo from the Duome website (https://duome.eu/vocabulary) using Playwright & creates a csv file



## 🔨 How to run 
1. Download `main.py` &amp; `requirements.txt` and put them inside a folder
2. Create a virtual environment: `python -m venv VEnv`
3. Activate virtual environment: 
    - 🪟 Windows CMD:
      
      ```
        VEnv\Scripts\activate
      ```
    - 🐧 Linux:
      
      ```
        source VEnv/bin/activate
      ```
4. Install dependencies:
   
   ```
     pip install -r requirements.txt
   ```
6. Install playwright (⚠️ code uses Microsoft Edge browser, you can change that to chromium if you don't want to download `msedge`):
   
   ```
     playwright install && playwright install msedge
   ```
8. Read the code, you may need to personalize some variables, then run the `main.py` &amp; wait to get the final `.csv` file
9. Open Anki application...  
     **File** ➡️ **Import...** ➡️ Choose .csv file

## ⚠️ Known (possible) issues
- If all word elements didn't load all at once, we should scroll down to retrieve all the words. However, this feature has not been implemented yet, as the 
