# Health Care Data Mining

## TEST RUN

1. Install Apache Solr and create a core named 'healthcare'. We need it for indexing and analysing data
2. Index data in Apache Solr. Run services/query.py file by changing the data file if needed on line 11 and call the create() method
3. Start Apache Solr with command ```solr start```
4. Start the flask app by running the api/driver.py file
5. Open views/index.html file on a web browser
6. Enter search query. (currently searching the 'content' field in the posts scraped. Could be changed accordingly)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.