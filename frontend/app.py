#!/usr/bin/env python3
import os, uuid
import time
from flask import Flask, render_template, jsonify
from urllib.request import urlopen 
import requests
from requests.exceptions import HTTPError
import json
import logging

app = Flask(__name__)

SERVICE_X = os.getenv("SERVICE_X", "localhost")
SERVICE_X_PORT = os.getenv("SERVICE_X_PORT", "6000")


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')


@app.route('/list')
def ws_page():
    try:
        response = requests.get(('http://{0}:{1}/api/v1/resources/books/all').format(SERVICE_X,SERVICE_X_PORT))
        response.raise_for_status()
        Jresponse = response.text
        data = json.loads(Jresponse)
        print("Entire JSON response")
        print(data)
        svcres_ = requests.get(('http://{0}:{1}/api/v1/resources/users/all').format(SERVICE_X,SERVICE_X_PORT))
        Jresponse1 = svcres_.text
        data1 = json.loads(Jresponse1)
        print("Entire JSON response")
        print(data1)
        #return jsonify(data)
        return render_template('ws.html', jdt=data, jdt1=data1 )

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return "Somethig is wrong. You should check backend Microservice call!"
        
    except Exception as err:
        print(f'Other error occurred: {err}')
        return "Somethig is wrong. You should check backend Microservice call!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
