#!/bin/zsh
#rsync -av -e ssh --exclude='.git' --exclude='.idea' --exclude='data' --exclude="drugbank_docs" ./ ubuntu@prepaire.net:/home/ubuntu/prepaire/
rsync -av -e ssh --exclude='.git' --exclude='.idea' --exclude='data' ./ ubuntu@ec2-3-123-29-32.eu-central-1.compute.amazonaws.com:/home/ubuntu/prepaire/
#scp -r -i ~/.ssh/prepaire-ubuntu.pem vicent/* ubuntu@ec2-52-57-137-117.eu-central-1.compute.amazonaws.com:/home/ubuntu/prepaire/
