import os
import enum
import secrets

from dataclasses import dataclass
from flask import Flask, Response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from cryptos import Bitcoin
from eth_account import Account as EthereumAccount


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)
app.config['WTF_CSRF_ENABLED'] = False

db = SQLAlchemy(app)


class CryptocurrencyAcronym(enum.Enum):
    BITCOIN = 'BTC'
    ETHEREUM = 'ETH'


@dataclass
class PrivateKey(db.Model):
    __tablename__ = 'private_key'

    value: str

    id = Column(Integer, primary_key=True)
    value = Column(String(250), nullable=False)

    def __init__(self, value):
        self.value = value


@dataclass
class CryptoAddress(db.Model):
    __tablename__ = 'crypto_address'
    __allow_unmapped__ = True

    id: int
    address: str
    acronym: str
    private_key: PrivateKey

    id = Column(Integer, primary_key=True)
    address = Column(String(250), nullable=False)
    acronym = Column(String(3), nullable=False)
    private_key_id = Column(Integer, ForeignKey('private_key.id'))
    private_key = relationship("PrivateKey")

    def __init__(self, address, acronym, private_key_id):
        self.address = address
        self.acronym = acronym
        self.private_key_id = private_key_id

    def __repr__(self):
        return f'<CryptoAddress {self.address}>'


def get_or_generate_private_key(private_key):
    if not private_key:
        private_key = secrets.token_hex(32)

    return private_key


def generate_btc_address(private_key):
    btc = Bitcoin(testnet=True)
    public_key = btc.privtopub(private_key)
    btc_address = btc.pubtoaddr(public_key)

    return btc_address


def generate_eth_address(private_key):
    eth = EthereumAccount.from_key(private_key)
    return eth.address


@app.route('/generate_address', methods=['POST'])
def generate_address():
    acronym = request.json.get('acronym')
    if acronym not in [CryptocurrencyAcronym.ETHEREUM.value, CryptocurrencyAcronym.BITCOIN.value]:
        return Response(
            "Invalid or missing value for 'acronym' parameter. Supported values: 'BTC' and 'ETH'", 400
        )

    private_key = PrivateKey(get_or_generate_private_key(None))
    db.session.add(private_key)
    db.session.flush()

    address = None
    if acronym == CryptocurrencyAcronym.BITCOIN.value:
        address = generate_btc_address(private_key.value)

    if acronym == CryptocurrencyAcronym.ETHEREUM.value:
        address = generate_eth_address(private_key.value)

    crypto_address = CryptoAddress(address, acronym, private_key.id)
    db.session.add(crypto_address)
    db.session.commit()

    return jsonify({'address': crypto_address.address})


@app.route('/list_address', methods=['GET'])
def list_address():
    crypto_addresses = CryptoAddress.query.all()
    return jsonify(crypto_addresses)


@app.route('/retrieve_address/<int:address_id>', methods=['GET'])
def retrieve_address(address_id):
    crypto_address = CryptoAddress.query.get(address_id)
    return jsonify(crypto_address)


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
