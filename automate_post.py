import boto3
from boto3.dynamodb.conditions import Key
import datetime
from re import sub
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Posts
import yaml
import os


with open('config.yml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

with open(os.path.dirname(os.path.realpath(__file__)) + '/content/content.txt',
          'r') as file:
    post_content = file.read()

with open(os.path.dirname(os.path.realpath(__file__)) + '/content/heading.txt',
          'r') as file:
    heading = file.read()


# Service shit
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(cfg['dynamodb']['name'])

now = datetime.datetime.now()


def get_dynamodb_items(dynamo_table):
    response = dynamo_table.query(KeyConditionExpression=Key('Date')
                                  .eq(now.strftime("%Y-%m-%d")))
    return response['Items']


def create_mysql_session(user, pw, host, db):
    connection_string = 'mysql+pymysql://{0}:{1}@{2}/{3}'\
        .format(user, pw, host, db)
    engine = create_engine(connection_string)
    session = sessionmaker(bind=engine)
    return session()


def create_post(items):
    post_title = "Alexa Voice Deals for " + now.strftime("%B %d,%Y")
    post_name = "alexa-deals-" + now.strftime("%B").lower() + "-" + \
                now.strftime("%d") + "-" + now.strftime("%Y")
    guid='https://alexaready.com/deals/{0}'.format(post_name)
    post = heading
    for item in items:
        old_price = item['BuyPrice']
        new_price = item['FinalPrice']
        old_price_number = Decimal(sub(r'[^\d.]', '', old_price))
        new_price_number = Decimal(sub(r'[^\d.]', '', new_price))
        url = 'amazon.com'
        percentage = round((1 - new_price_number/old_price_number) * 100, 0)
        section = post_content.format(item['IMG'], url, item['Utterance'],
                                      item['FinalPrice'], item['BuyPrice'],
                                      percentage, item['Utterance'],
                                      item['Title'])
        post = post + section

    return Posts(post_date=now, post_date_gmt=now, post_content=post,
                 post_modified=now, post_modified_gmt=now, guid=guid,
                 post_title=post_title, post_name=post_name)


def write_post(session, post):
    session.add(post)
    session.commit()


def lambda_handler(event, context):
    print('Getting items from dyamodb')
    items = get_dynamodb_items(table)
    print('There are {0} products'.format(len(items)))
    post = create_post(items)
    print('Post created')
    session = create_mysql_session(cfg['mysql']['user'],
                                   cfg['mysql']['password'],
                                   cfg['mysql']['host'], cfg['mysql']['db'])
    write_post(session, post)
    print('Post written to Wordpress')


if __name__ == "__main__":
    print('Getting items from dyamodb')
    items = get_dynamodb_items(table)
    print('There are {0} products'.format(len(items)))
    post = create_post(items)
    print('Post created')
    session = create_mysql_session(cfg['mysql']['user'],
                                   cfg['mysql']['password'],
                                   cfg['mysql']['host'], cfg['mysql']['db'])
    print('Connected to MySQL Database')
    write_post(session, post)
    print('Post written to Wordpress')
