# Data-Scraping with typer CLI

## install following Python Libraries

```
python -m pip install selenium
python -m pip install pandas
python -m pip install requests
python -m pip install BeautifulSoup4
python -m pip install datetime
python -m pip install typer
python -m pip install deep_translator
```

### run with python
```
python .\main.py thbuththegama-dec-prices
python .\main.py dambulla-dec-prices 
```
#### Select item price according to text file
```
python .\main.py text-to-list file thabuththegama
python .\main.py text-to-list items dambulla
```
replace '_file_' with your file name


### Install Typer-CLI
`python -m pip install typer-cli`

### Enable auto completion for your terminal
`typer --install-completion`

### run with typer cli

```
typer .\main.py run thbuththegama-dec-prices
typer .\main.py run dambulla-dec-prices 

typer .\main.py run text-to-list items dambulla
typer .\main.py run text-to-list file thabuththegama
``` 
**Note that text file should be in the same directory as main.py**

# text-to-list items dambulla not return any values. Need to fix it #
