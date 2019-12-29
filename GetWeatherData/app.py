import json
from zeep import Client
from datetime import datetime, timedelta
DATE_FORMAT = '%Y-%m-%d'
url = 'https://www.wcc.nrcs.usda.gov/awdbWebService/services?WSDL'
client = Client(url)

def dates_from_days(num_days):
    end_date = datetime.today().strftime(DATE_FORMAT) + ' 23:59'
    begin_date = (datetime.today() - timedelta(days=num_days)).strftime(DATE_FORMAT)
    return begin_date, end_date

def process_response(data):
    return [obj.dateTime for obj in data[0].values],[int(obj.value) for obj in data[0].values]
        
def call_api(snotel_site_name, num_days):
    # element codes: 
    # TOBS = AIR TEMPERATURE OBSERVED
    # PREC = PRECIPITATION ACCUMULATION
    # SNWD = SNOW DEPTH
    # WTEQ = SNOW WATER EQUIVALENT
    # WSPDX = WIND SPEED MAXIMUM
    # WDIRV = WIND DIRECTION AVERAGE
    begin_date, end_date = dates_from_days(num_days)
    element_codes = ['TOBS', 'PREC', 'SNWD', 'WTEQ','WSPDX', 'WDIRV']
    results = []
    for index, element in enumerate(element_codes):
        data = {
            'stationTriplets': snotel_site_name,
            'elementCd':element,
            'ordinal':1,
            'beginDate':begin_date,
            'endDate':end_date
        }
        results.append(process_response(client.service.getHourlyData(**data)))
    return results
        
        


def lambda_handler(event, context):
    print(event)
    return {
        "isBase64Encoded": 'false',
        "statusCode": 200,
        "headers": {'Access-Control-Allow-Origin':'*'},
        "body": json.dumps(call_api(event['queryStringParameters']['snotel'],int(event['queryStringParameters']['days'])))
    }
