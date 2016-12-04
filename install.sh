#!/usr/bin/env bash
echo "Installing psycopg2 dependencies..."
sudo apt-get install libpq-dev python-dev
echo "Installing psycopg2..."
sudo pip3 install psycopg2
echo "psycopg2 installed"
echo "Installing utils dependencies..."
sudo pip3 install python-dateutil
echo "Done."
exit 0