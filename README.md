# DuoScraper
<center>
  <img src="https://i.postimg.cc/W14rPY3b/Duolingo-In-Love-With-Anki.png" width="200" height="150">
</center>

This project scrapes any languages available on Duolingo from the Duome website (https://duome.eu/vocabulary) using Playwright & creates a csv file



## 🔨 How to run


  <ol start="0">
  <li>Download <code>main.py</code> &amp; <code>requirements.txt</code> and put them inside a folder</li>
  <li>Create a virtual environment:
    <pre><code>python -m venv VEnv
    </code></pre>
  </li>
  <li>Activate virtual environment:
    <ul>
      <li>🪟 Windows CMD:
        <pre><code>VEnv\Scripts\activate
        </code></pre>
      </li>
      <li>🐧 Linux:
        <pre><code>source VEnv/bin/activate
        </code></pre>
      </li>
    </ul>
  </li>
  <li>Install dependencies:
    <pre><code>pip install -r requirements.txt
    </code></pre>
  </li>
  <li>Install playwright (⚠️ code uses Microsoft Edge browser, you can change that to chromium if you don't want to download <code>msedge</code>):
    <pre><code>playwright install &amp;&amp; playwright install msedge
    </code></pre>
  </li>
  <li>Read the code, you may need to personalize some variables, then run the <code>main.py</code> & wait to get the final <code>.csv</code> file</li>
  <li>
    Open Anki application...<br>
    On Android: From top-right, click on <b>⋮</b> and select <b>Import</b><br>
    On Desktop: <b>File</b> ➡️ <b>Import...</b> ➡️ Choose .csv file
  </li>
</ol>

</details>



## ⚠️ Known (possible) issues
- If all word elements didn't load all at once, we should scroll down to retrieve all the words. However, this feature has not been implemented yet, as the 

