#!/usr/bin/env bash

set -e

## Fixture
# Transfer images to media folder

# Database migrations
echo " "
echo "...................................."
echo "Applying database migrations ..."
python manage.py migrate

# # Test Pipeline
# echo " "
# echo "Apply test pipeline"
# python -m pytest
# echo " "

## Fixture
# Create specific folders
mkdir -p ./media/product/T-Shirt
mkdir -p ./media/product/Cap

# Transfer images to media folder
find ./fixture-images -iname '*t-shirt*' -exec cp {} ./media/product/T-Shirt/ \;
find ./fixture-images -iname '*cap*' -exec cp {} ./media/product/Cap/ \;

echo " "
echo "...................................."
echo "Applying fixtures ..."
python manage.py custom_load_fixture
echo " "


$@