# README #
To install requirements you should run next command:
```
make install
```

To start the Application use a command:
```
make start
```

To run tests use command:
```
python3 app/tests.py
```


Availables APIs:

1. Generate Address. Required param name of Cryptocurrency acronym. 'ETH' and 'BTC' are supported.

Request:
```
POST http://127.0.0.1:8000/generate_address
POST Data:
{
    "acronym": "BTC"
}
```

Response:
```
{
    "address": "mp5LhCeLjHSRTw2pqRgVkMk2WzbF5e1aux"
}
```



2. List Address. Returns a list of all the addresses generated so far.

Request:
```
GET http://127.0.0.1:8000/list_address
```
Response:
```
[
    {
        "acronym": "BTC",
        "address": "mhSeCKbEMsAJxkbSDR8Pdx7GQfEK16Zmxk",
        "id": 6,
        "private_key": {
            "value": "9e8bc8fcb2c1d2a550e83720f0e814bb8415b2abd5ba61905216c791499179c4"
        }
    },
    {
        "acronym": "ETH",
        "address": "0x74e1727F84ede0E46B0Fe3b899a7E46d36244b6f",
        "id": 7,
        "private_key": {
            "value": "4c0970e90d731f032fa8c216851d0b318a29122c5ff27b60119108d287300858"
        }
    }
]
```


3. Retrieve Address. Return a created address by id.

Request:
```
http://127.0.0.1:8000/retrieve_address/1
```
Response:
```

{
    "acronym": "BTC",
    "address": "mo8asK7MWMWE6bUzW7w9q4T9LdHh2aoNTj",
    "id": 1,
    "private_key": {
        "value": "871902c28f69845884b0c41f0739c82120ce06a859e890dbdc323c716941b817"
    }
}
```
