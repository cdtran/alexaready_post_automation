import boto3
from boto3.dynamodb.conditions import Key
import datetime
from re import sub
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Posts
import yaml


with open('config.yml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile)


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

(cfg['mysql']['user'], cfg['mysql']['password'],
                cfg['mysql']['host'], cfg['mysql']['db'])


def create_post(items):
    post_title = "Alexa Voice Deals for " + now.strftime("%B %d,%Y")
    post_name = "alexa-deals-" + now.strftime("%B").lower() + "-" + \
                now.strftime("%d") + "-" + now.strftime("%Y")

    post_heading = "[et_pb_section bb_built=\"1\" fullwidth=\"off\" specialty=\"off\"][et_pb_row][et_pb_column type=\"4_4\"][et_pb_text admin_label=\"The Deals Intro\" _builder_version=\"3.0.89\" background_layout=\"light\"] \n\n<h1>The Deals</h1> \nBelow you’ll find the latest deals exclusive to your Amazon Alexa device. To order, simply say the command to Alexa. Alexa will handle the rest. \nTo learn more about each product, click on the image or visit the ‘Learn more on Amazon’ link. We added our two cents to each of the products. Let us know what you think! Happy saving!"

    for item in items:
        old_price = item['BuyPrice']
        new_price = item['FinalPrice']
        old_price_number = Decimal(sub(r'[^\d.]', '', old_price))
        new_price_number = Decimal(sub(r'[^\d.]', '', new_price))
        percentage = round((1 - new_price/old_price) * 100, 0)
        text = "[ / et_pb_text][ / et_pb_column][ / et_pb_row][ / et_pb_section][et_pb_section bb_built = \"1\" admin_label = \"Alexa Voice Deal\" fullwidth = \"off\" specialty = \"on\" _builder_version = \"3.0.89\" make_fullwidth = \"on\"][et_pb_column type = \"1_3\"][et_pb_image admin_label = \"Product Image\" _builder_version = \"3.0.89\" src = " + items['IMG'] + " show_in_lightbox = \"off\" url = \"http://amzn.to/2A9Vtor\" url_new_window = \"on\" use_overlay = \"off\" always_center_on_mobile = \"on\" force_fullwidth = \"off\" show_bottom_space = \"on\" /][ / et_pb_column][et_pb_column type = \"2_3\" specialty_columns = \"2\"][et_pb_row_inner admin_label = \"Row\"][et_pb_column_inner type = \"1_2\" saved_specialty_column_type = \"2_3\"][et_pb_text admin_label = \"Product Title\" _builder_version = \"3.0.89\" background_layout = \"light\"] < h2 > " + item['Utterance'] + " < / h2 > < h3 >" + new_price + " < / h3 > Sale: " + old_price + ", Save " + percentage + " % [ / et_pb_text][ / et_pb_column_inner][et_pb_column_inner type = \"1_2\" saved_specialty_column_type = \"2_3\"][et_pb_testimonial admin_label = \"Alexa Quote\" background_layout = \"light\" _builder_version = \"3.0.89\" custom_css_testimonial_author = \"display: none;\" custom_css_testimonial_meta = \"display: none;\" text_orientation = \"center\" url_new_window = \"off\" quote_icon = \"on\" use_background_color = \"on\" quote_icon_background_color = \"#f5f5f5\" portrait_border_radius = \"21\" saved_tabs = \"all\" border_radii_portrait = \"21\"] < p style = \"margin: 0 auto;\" > " + item['Utterance'] + " < / p >" \
                                                               "[ / et_pb_testimonial][ / et_pb_column_inner][ / et_pb_row_inner][et_pb_row_inner admin_label = \"Row\"][et_pb_column_inner type = \"4_4\"" \
                                                               "saved_specialty_column_type = \"2_3\"][et_pb_text admin_label = \"Two Cents\"" \
                                                               "_builder_version = \"3.0.89\"" \
                                                               "background_layout = \"light\"] " + item['Title'] + "[ / et_pb_text][ / et_pb_column_inner][ / et_pb_row_inner][ / et_pb_column][ / et_pb_section][et_pb_section bb_built = \"1\"" \
        "admin_label = \"Alexa Voice Deal\"" \
        "fullwidth = \"off\" specialty = \"on\" _builder_version = \"3.0.89\" make_fullwidth = \"on\"][et_pb_column type = \"1_3\"][et_pb_image admin_label = \"Product Image\"_builder_version = \"3.0.89\" show_in_lightbox = \"off\" url_new_window = \"on\" use_overlay = \"off\" always_center_on_mobile = \"on\" force_fullwidth = \"off\" show_bottom_space = \"on\" /][ / et_pb_column][et_pb_column type = \"2_3\" specialty_columns = \"2\"][et_pb_row_inner admin_label = \"Top Row\" _builder_version = \"3.0.89\"][et_pb_column_inner type = \"1_2\" saved_specialty_column_type = \"2_3\"][et_pb_text admin_label = \"Product Title\" _builder_version = \"3.0.89\" background_layout = \"light\"]"
        post_heading = post_heading + "\n\n" + text

    return Posts(post_date=now, post_date_gmt=now, post_content=post_heading,
                 post_title=post_title, post_name=post_name)


def write_post(session, post):
    session.add(post)
    session.commit()


def lambda_handler(event, context):
    items = get_dynamodb_items(table)
    create_post(items)

