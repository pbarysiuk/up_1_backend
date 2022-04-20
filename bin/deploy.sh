#!/bin/zsh
rsync -av -e ssh --exclude='.git' --exclude='venv' --exclude='.idea' --exclude='data' --exclude="drugbank_docs" ./ ubuntu@prepaire.net:/home/ubuntu/prepaire/

