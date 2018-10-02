requests-onshape
================
The bare necessities for using the [Onshape](https://www.onshape.com) API with [Requests](https://github.com/requests/requests).

## Installation
```sh
pip install requests-onshape
```

## Usage examples
```python
from requests_onshape import OnshapeSession

onshape = OnshapeSession(access_key="foo", secret_key="bar")
documents = onshape.get("documents", params={"limit": 1}).json()

encoded_configuration = onshape.post(
    "elements/d/foo/e/bar/configurationencodings",
    json={
        "parameters": [
            {"parameterId": "Height", "parameterValue": "200 mm"},
            {"parameterId": "Width", "parameterValue": "20 mm"},
        ]
    },
)
```
