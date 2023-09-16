#!/bin/bash

# Stop, delete and remove container image
docker stop beerify-api
docker rm beerify-api
docker rmi beerify-api-image
