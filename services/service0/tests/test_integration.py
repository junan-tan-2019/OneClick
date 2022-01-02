import json
import pytest


def call(client, path, method='GET', body=None):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }


    if method == 'PATCH':
        response = client.patch(path, data=json.dumps(body), headers=headers)
    else:
        response = client.get(path)

    return {
        "json": json.loads(response.data.decode('utf-8')),
        "code": response.status_code
    }

@pytest.mark.dependency()
def test_update_stock(client):
    result = call(client, 'stocks/update', 'PATCH', {
        "location": "Woodland CC"
    })
    assert result['code'] == 200
    assert result ['json']['data'] == {
            "id": 2,
            "location": "Woodland CC",
            "longitude": 1.43983,
            "latitude": 103.788,
            "stock": 194
    }