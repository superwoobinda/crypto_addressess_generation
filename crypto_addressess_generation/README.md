# README

## Installation

To install the required dependencies, run the following command:

```
make install
```

## Usage

To start the application, use the following command:

```
make start
```

## Running Tests

To run the tests, execute the following command:

```
python3 app/tests.py
```

## Available APIs

### 1. Generate Address

This API allows you to generate an address for a cryptocurrency. Currently, 'ETH' and 'BTC' are supported.

**Request:**

```
POST http://127.0.0.1:8000/generate_address
```

**Request Data:**

```json
{
    "acronym": "BTC"
}
```

**Response:**

```json
{
    "address": "mp5LhCeLjHSRTw2pqRgVkMk2WzbF5e1aux"
}
```

### 2. List Address

This API returns a list of all the addresses that have been generated so far.

**Request:**

```
GET http://127.0.0.1:8000/list_address
```

**Response:**

```json
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

### 3. Retrieve Address

This API retrieves the details of a created address based on its ID.

**Request:**

```
GET http://127.0.0.1:8000/retrieve_address/1
```

**Response:**

```json
{
    "acronym": "BTC",
    "address": "mo8asK7MWMWE6bUzW7w9q4T9LdHh2aoNTj",
    "id": 1,
    "private_key": {
        "value": "871902c28f69845884b0c41f0739c82120ce06a859e890dbdc323c716941b817"
    }
}
```
