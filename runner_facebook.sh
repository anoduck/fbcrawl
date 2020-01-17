#!/usr/local/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

source credentials.txt
source sites.txt

TIME=$(date +"%Y-%m-%d_%H-%M")
DATE=$(date +"%Y-%m-%d")

for site in $sites
do
    echo " "
    echo "************* Current page: $site ***************************************"
    mkdir -p "../res/$site/"
   
    scrapy crawl fb -a email="$FACEBOOK_EMAIL" -a password="$FACEBOOK_PASSWORD" -a page="$site" -a lang="en" -o "../res/$site/posts/$TIME.csv" -a date="$DATE" 
    
    scrapy crawl comments -a email="$FACEBOOK_EMAIL" -a password="$FACEBOOK_PASSWORD" -a page="$site" -a lang="en" -o "../res/$site/comments/$TIME.csv" -a date="$DATE" 

done

echo " "
echo "************* finished. ****************************************************"
