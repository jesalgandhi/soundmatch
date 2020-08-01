# soundmatch
Flask-based webapp created for final CS50 project, that helps you find a broader range of free sounds at ease.

### How does it work?
Soundmatch works by taking an inputted word from a user, such as 'hammer' or 'explosion' for example, and passes it though the <a href="https://www.datamuse.com/api/">Datamuse API</a>. Using the 'Means like constraint' provided by Datamuse, synonyms of this word are then found. The amount of synonyms (and subsequent matching sound results) are determined by whether the user picks 'Less', 'More', or 'Most' when inputting. 

After receiving the input, the amount of results, and the list of synonyms, these synonym strings are then passed through the <a href="https://freesound.org/apiv2/">Freesound API</a>, using the <a href="https://github.com/MTG/freesound-python">Python</a> client. Freesound generates 5, 10, or 15 sound ID's (depending on user input) for each synonym, and then returns these results to the user in the form of embedded `<iframe>`s (although this is not ideal, it was the only practical way I found I could allow the user to display and seek through the sounds without downloading them on either end). 

You can then click "Add to My Sounds" on any desired sound(s), and after saving to your sounds, they will be under "My Sounds" in the navbar. Under "My Sounds" you can choose to download a sound or remove it from your list.


### Why?
Although freesound offers a wide array of both amateur and professional sounds, I found that their search function rarely returns what I am looking for. I also realized that, oftentimes, when searching for a specific or particular sound, I cannot find it because it is indexed under a different name. Therefore, with soundmatch, I hope to bridge the gap between what sounds a user is looking for by showing them not only sounds from their particular search, but also related sounds. Think of it sort of like a <a href="https://en.wikipedia.org/wiki/Approximate_string_matching">fuzzy search</a>.

### Screenshots


### Instructions to run locally
To do this, start by clonining or downloading this project. 

After this, you will need to use a Terminal to actually run the web server locally. I tried doing this on Windows via PowerShell, but it was giving me problems, so I would recommend using Git Bash. To install Git Bash, simply intall git from <a href="https://git-scm.com/">here</a> and make sure to install Git Bash as well during the installation window (select 'Git from the command line and also from 3rd-party software' option). For macOS/Unix users, just use the integrated Terminal.

Traverse to the directory where you have stored the `soundmatch` folder (in my case it's `~/desktop/files/soundmatch`). The first thing you must do is set up the api key so you can make requests to the freesound api. Click <a href="https://freesound.org/help/developers/">Here</a> to sign up for a free account and get an api key. Once that is done, run the following command in your Terminal window:
```
export API_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```
where `XXXXXXXXXXXXXXXXXXXXXXXXXXXXX` is your api key. 

Then use the following command to actually run the flask app:
```
flask run
```

The server should now be up and running, and a localized link will tell you where it is running. Try out the site and have fun! Run the command `CTRL+C` to exit out of the flask app.

### Demo
Unfortunately, to host this project to Heroku, I need to convert my cs50 sql instances to SQLAlchemy instances instead, and it will take some time to learn this new technology. If there is enough interest/I get extra time, I will try my best to host this website for all to try :)
