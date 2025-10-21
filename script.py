import json
import logging
import os
from flask import Flask, jsonify, request, render_template, session
from tb_rest_client.rest_client_pe import *
import re
from openai import OpenAI
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

TB_URL = "https://dashboard.iot.undp.org"
USERNAME = 
PASSWORD = 
with RestClientPE(base_url=TB_URL) as rest_client:
    rest_client.login(username=USERNAME, password=PASSWORD)
    dashboard = rest_client.get_user_dashboards()
    #save this as json file , that will be your data file
    