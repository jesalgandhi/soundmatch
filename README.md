# soundmatch
Flask-based webapp created for final CS50 project, that helps you find a broader range of free sounds at ease.

### How does it work?
Soundmatch works by taking an inputted word from a user, such as 'hammer' or 'explosion' for example, and passes it though the <a href="https://www.datamuse.com/api/">Datamuse API</a>. Using the 'Means like constraint' provided by Datamuse, synonyms of this word are then found. The amount of synonyms (and subsequent matching sound results) are determined by whether the user picks 'Less', 'More', or 'Most' when inputting. 

After receiving the input, the amount of results, and the list of synonyms, these synonym strings are then passed through the <a href="https://freesound.org/apiv2/">Freesound API</a>, using the <a href="https://github.com/MTG/freesound-python">Python</a> client. Freesound generates 5, 10, or 15 sound ID's (depending on user input) for each synonym, and then returns these results to the user in the form of embedded `<iframe>`s (although this is not ideal, it was the only practical way I found I could allow the user to display and seek through the sounds without downloading them on either end). 

You can then click "Add to My Sounds" on any desired sound(s), and after saving to your sounds, they will be under "My Sounds" in the navbar. Under "My Sounds" you can choose to download a sound or remove it from your list.


### Why?
Although freesound offers a wide array of both amateur and professional sounds, I found that their search function rarely returns what I am looking for. I also realized that, oftentimes, when searching for a specific or particular sound, I cannot find it because it is indexed under a different name. Therefore, with soundmatch, I hope to bridge the gap between what sounds a user is looking for by showing them not only sounds from their particular search, but also related sounds. Think of it sort of like a <a href="https://en.wikipedia.org/wiki/Approximate_string_matching">fuzzy search</a>.

