#!/bin/sh

curl -s -G "https://api.hh.ru/vacancies?text=${1/ /+}E&per_page=20" | jq > hh.json
