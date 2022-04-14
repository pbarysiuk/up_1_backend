
# Prepaire Backend

API to retrieve information from drugbank, natural products
and execute AI models.


## Tech Stack

**Client:** React, Material-ui (mui)

**Server:** Python, Flask, MongoDB


## Dependencies

Dependencies to run the project

```
docker
docker-compose
```

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

There is a .env.example to copy from


`MONGO_INITDB_ROOT_USERNAME`

`MONGO_INITDB_ROOT_PASSWORD`

`MONGODB_CONNSTRING`


## Run Locally

Clone the project

```bash
  git clone git@github.com:jordiigarciaa/Prepaire_back.git
```

Go to the project directory

```bash
  cd Prepaire_back
```

Install dependencies && Start the server

```bash
  ./bin/start
  or
  docker-compose build && docker-compose up -d && docker-compose logs -f  
```

Sometimes api stops due to changes. To start only api, execute
```bash
  docker-compose up -d api
```


## Getting Started
Open a browser with http://localhost:5000 to see available options.
To set up initial DB, you can get some documents for drugbank at http://prepaire.net:5000/document/DB01234
changing DB01234 for range 00001 to 15000.

Save documents at drugbank_docs at root of the project.

Execute ```GET http://localhost:5000/drugbank/import```

Download natural_products from http://oolonek.github.io/ISDB/ and use cat UNPD_DB.csv_* >> UNPD_DB.csv.
Put this file into src/natural_products

Execute ```GET http://localhost:5000/natural_products/import```

To import lotus natural products, you'll need to connect through mongo and restore table lotusUniqueNaturalProduct
Execute 
```bash
mongorestore -u AzureDiamondUsername --authenticationDatabase admin --db drugbank --collection lotusUniqueNaturalProduct --noIndexRestore lotusUniqueNaturalProduct.bson
mongo -u AzureDiamondUsername
db.lotusUniqueNaturalProduct.createIndex( {smiles: "hashed"})
db.runCommand(
  {
    createIndexes: 'lotusUniqueNaturalProduct',
    indexes: [
        {
            key: {
                iupac_name:"text", traditional_name:"text", allTaxa:"text"
            },
            name: "superTextIndex",
	    weights: { name:10, synonyms:5  }
        }

    ]
  }
)
```
## Deployment

To deploy this project run

```bash
  ./bin/deploy
```

*You must have the proper .pem


## Modules

- Drugbank
- Natural Products
- AI - Models
  - Solubility
  - Toxicity


## Authors

- [@jordiigarciaa](https://www.github.com/jordiigarciaa)

