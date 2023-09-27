import asyncio
import httpx
import requests
import json
import os

from dotenv import load_dotenv
from httpx import AsyncClient

from flask import (
    Blueprint, jsonify, request, render_template, redirect, url_for
)

bp = Blueprint('home', __name__)

load_dotenv()


APP_TOKEN = os.getenv('APP_TOKEN')
BASE_URL = ('https://data.austintexas.gov/resource/fdj4-gpfu.json?'
            '$$app_token={}').format(APP_TOKEN)
COUNT = '&$select=count(incident_report_number) as count'
QUERY = '&$select=rep_date,address,crime_type&$order=rep_date DESC&$limit=1'

zs = ['78741', '78704', '78724']


async def async_count_matches(i, session):
    url = BASE_URL + COUNT + '&zip_code={}'.format(i)
    res = await session.get(url)
    data = res.json()
    print(data[0]['count'])


def count_matches(z):
    url = BASE_URL + COUNT + '&zip_code={}'.format(z)
    res = requests.get(url)
    data = res.json()
    return data[0]


async def return_data(o: int, z: int, session: AsyncClient):
    url = BASE_URL + QUERY + '&$offset={}&zip_code={}'.format(o, z)
    res = await session.get(url)
    data = res.json()
    print(data[0]['address'])
    return data[0]


@bp.route('/', methods=('GET', 'POST'))
async def index():
    if request.method == 'POST':
        z = request.form['zipcode']
        # return f'<h1>{z}</h1>'
        count = count_matches(z)
        c = int(count['count'])
        async with httpx.AsyncClient() as session:
            res = await asyncio.gather(*(return_data(o, z, session) for o in range(c // 1000)))
            return res

    
    return render_template('home/home.html')