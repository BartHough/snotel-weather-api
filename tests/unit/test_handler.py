import json

import pytest

from GetWeatherData import app


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "queryStringParameters": {
            "snotel_site": "322:CO:SNTL",
            "days": "30",
            "element_code": "WDIRV"
        }
    }


def test_lambda_handler(apigw_event, mocker):

    ret = app.lambda_handler(apigw_event, "")
    assert ret["statusCode"] == 200
    assert ret["body"]
