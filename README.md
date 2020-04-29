# Health Care Data Mining

## Outline
Provide a user interface to query user posts by topic, symptoms, diseases, and other filtering parameters such as allowing users to query by the website that they want to see results from, etc. The application consists of a backend infrastructure and a front-end UI. These are present in the Code folder. In order to run the application, we need to ensure that the following packages and frameworks are installed. We provide the installation manual for a mac system.

### Step1: Install python3 and pip

```
brew install python3
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

### Step2: Install Apache Solr

```
brew install solr
```
For the full installation guide from a tar or zip, [refer the official website.](https://lucene.apache.org/solr/guide/8_5/installing-solr.html)


## User Interface

![Alt text](arch.png?raw=true "User Interface")

## Starting the Application


### Create core in Apache Solr and Index data in it

Start Apache Solr by using
```
solr start
```
For more details, for these [instructions](https://www.tutorialspoint.com/apache_solr/apache_solr_core.htm)

```
./solr create -c Solr_sample 
```
Use the Solr/solr.py file or the services/query.py file to index data in Apache solr using the data files present in the data directory.


### Backend app

To start the application, first, navigate to the api folder from the project root. Run ```python3 driver.py``` to start a server on port 5000 by default.

### Frontend app

Navigate to the views folder and open the index.html file in a web browser. You will then see the above UI. Enter the search query for either diseases or symptoms to get the relevant posts. 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.