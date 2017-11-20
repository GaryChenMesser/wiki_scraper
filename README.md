# wiki_scraper
This is a scraper which can start from a specific page, scraping outward, record the network structure and finally output a gdf file describing the network relation.

## Usage
The scraper can only detect whether the outward page is about a person or not. Other classifications will be include in a few days.
* ```--person``` is to specify a person's name, which is the page name you want to go. 
* ```--steps``` is to specify the step you want to hop from the page you specify above.
### Example:
```commend line
python3 wiki_scraper.py --person Barack_Obama --steps 2
```
