build_tx_components_schema = {
            "address_origin": {
                "type": "string",
                "required": True,
            },
            "address_destin": {
                "type": "list",
                "dependencies": "address_origin",
                "required": False,
                "schema": {
                    "type": "dict",
                    "schema": {
                        "address": {"type": "string", "required": True},
                        "amount": {"type": "integer", "dependencies": "address"},
                        "tokens": {
                            "type": "list",
                            "required": False,
                            "dependencies": "address",
                            "schema": {
                                "type": "dict",
                                "schema": {
                                    "name": {"type": "string", "required": True},
                                    "amount": {"type": "integer", "required": True, "dependencies": "name"},
                                    "policyID": {"type": "string", "required": True, "dependencies": "name"},
                                },
                            },
                        },
                    },
                },
            },
            "change_address": {
                "type": "string",
                "required": False,
                "dependencies": "address_origin",
            },
            "metadata": {
                "type": "dict",
                "required": False,
                "dependencies": "address_origin",
            },
            "mint": {
                "type": "dict",
                "required": False,
                "dependencies": "address_origin",
                "schema": {
                    "action": {"type": "string", "required": True, "allowed": ["burn", "mint"]},
                    "tokens": {
                        "type": "list",
                        "required": False,
                        "schema": {
                            "type": "dict",
                            "schema": {
                                "name": {"type": "string", "required": True},
                                "amount": {"type": "integer", "required": True, "dependencies": "name"},
                                "policyID": {"type": "string", "dependencies": "name", "required": True}
                            },
                        },
                    },
                },
            },
            "script_path": {
                "type": "string",
                "required": False,
            },
            "witness": {
                "type": "integer",
                "required": False,
                "dependencies": "address_origin",
            },
            "inline_datum":{
                "type": "dict",
                "required": False,
                "dependencies": "address_origin",
            } 
        }

create_simple_script_schema = {
    "type": {
        "type": "string",
        "required": True,
        "empty": False,
        "allowed": ["all", "any", "atLeast"],
    },
    "required": {
        "type": "integer",
        "required": False,
        "empty": False,
        "dependencies": {"type":["atLeast"]},
        "min": 1,
    },
    "hashes": {
        "type": "list",
        "required": True,
    },
    "type_time": {
        "type": "string",
        "required": False,
        "empty": False,
        "allowed": ["before", "after"],
        "dependencies": "slot"
    },
    "slot": {
        "type": "integer",
        "required": False,
        "empty": False,
        "dependencies": "type_time"
    },
    "purpose": {
        "type": "string",
        "required": True,
        "allowed": ["mint", "multisig", "plutus"],
    }
}