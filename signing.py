from eth_account.messages import encode_structured_data
from eth_account import Account

def build_points_payload(account, ts):
    full_data = {
    "types": {
        "EIP712Domain": [
            {
                "name": "name",
                "type": "string"
            },
            {
                "name": "version",
                "type": "string"
            },
            {
                "name": "chainId",
                "type": "uint256"
            },
            {
                "name": "verifyingContract",
                "type": "address"
            }
        ],
        "Hyperliquid:UserPoints": [
            {
                "name": "hyperliquidChain",
                "type": "string"
            },
            {
                "name": "time",
                "type": "uint64"
            }
        ]
    },
    "primaryType": "Hyperliquid:UserPoints",
    "domain": {
        "name": "HyperliquidSignTransaction",
        "version": "1",
        "chainId": 1,
        "verifyingContract": "0x0000000000000000000000000000000000000000"
    },
    "message": {
        "type": "userPoints",
        "time": ts,
        "signatureChainId": "0x1",
        "hyperliquidChain": "Mainnet"
    }
}

    # Encode the structured data
    encoded_data = encode_structured_data(full_data)

    # Sign the encoded data
    signed_message = account.sign_message(encoded_data)

    r = hex(signed_message.r)
    s = hex(signed_message.s)
    v = signed_message.v

    request_data = {
        "signature": {
            "r": r,
            "s": s,
            "v": v
        },
        "signatureChainId": "0x1",
        "timestamp": ts,
        "type": "userPoints2",
        "user": account.address
    }
    # print(request_data)

    return request_data


def build_tos_payload(account, ts):
    ts = ts * 1000
    full_data = {
    "types": {
        "EIP712Domain": [
            {
                "name": "name",
                "type": "string"
            },
            {
                "name": "version",
                "type": "string"
            },
            {
                "name": "chainId",
                "type": "uint256"
            },
            {
                "name": "verifyingContract",
                "type": "address"
            }
        ],
        "Hyperliquid:AcceptGenesis": [
            {
                "name": "hyperliquidChain",
                "type": "string"
            },
            {
                "name": "message",
                "type": "string"
            },
            {
                "name": "genesisOption",
                "type": "string"
            },
            {
                "name": "time",
                "type": "uint64"
            }
        ]
    },
    "primaryType": "Hyperliquid:AcceptGenesis",
    "domain": {
        "name": "HyperliquidSignTransaction",
        "version": "1",
        "chainId": 1,
        "verifyingContract": "0x0000000000000000000000000000000000000000"
    },
    "message": {
        "type": "acceptGenesis",
        "message": "I agree to the [Genesis Event] Terms.",
        "genesisOption": "HYPE",
        "time": ts,
        "signatureChainId": "0x1",
        "hyperliquidChain": "Mainnet"
    }
}

    # Encode the structured data
    encoded_data = encode_structured_data(full_data)

    # Sign the encoded data
    signed_message = account.sign_message(encoded_data)

    r = hex(signed_message.r)
    s = hex(signed_message.s)
    v = signed_message.v

    request_data = {
        "genesisOption": "HYPE",
        "message": "I agree to the [Genesis Event] Terms.",
        "signature": {
            "r": r,
            "s": s,
            "v": v
        },
        "signatureChainId": "0x1",
        "time": ts,
        "type": "acceptGenesis",
        "user": account.address
    }
    # print(request_data)

    return request_data