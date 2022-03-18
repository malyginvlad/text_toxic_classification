# -*- coding: utf-8 -*-
import time
import logging
import requests


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    json_file = {'text': 'bad boy i hate him'}
    response = requests.get(
        "http://127.0.0.1:5000/analyze_text",
        json=json_file,
        verify=False,
        timeout=1,
    )
    print(response.json())
    logger.info(f"Status code: {response.status_code}\n")
    logger.info(f"Response body: {response.json()}\n")
