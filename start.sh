#!/bin/bash

docker build -t repayment-calc .

docker run -p 5006:5006 repayment-calc
