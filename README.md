# Prepaire_back


## Dependencies
- docker
- docker-compose
## Start
Execute ``` ./bin/start.sh```

## Getting Started
Open a browser with http://localhost:5000 to see available options.
To set up initial DB, you can get some documents for drugbank at http://prepaire.net:5000/document/DB01234
changing DB01234 for range 00001 to 15000.

Save documents at drugbank_docs at root of the project.

Execute ```GET http://localhost:5000/drugbank/import```

Download natural_products from http://oolonek.github.io/ISDB/ and use cat UNPD_DB.csv_* >> UNPD_DB.csv.
Put this file into src/natural_products

Execute ```GET http://localhost:5000/natural_products/import```

## Deploy
Execute ``` ./bin/deploy.sh```
