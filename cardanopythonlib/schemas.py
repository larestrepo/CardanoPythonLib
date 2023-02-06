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
                    "policyID": {"type": "string", "required": True},
                    "policy_path": {"type": "string", "required": True},
                    "validity_interval": {
                        "type": "dict",
                        "schema": {
                            "type": {"type": "string", "required": True},
                            "slot": {"type": "integer", "required": True},
                        },
                    },
                    "tokens": {
                        "type": "list",
                        "required": False,
                        "schema": {
                            "type": "dict",
                            "schema": {
                                "name": {"type": "string", "required": True},
                                "amount": {"type": "integer", "required": True, "dependencies": "name"},
                                "action": {"type": "string", "required": True, "dependencies": "name", "allowed": ["burn", "mint"]}
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
    "name": {
        "type": "string",
        "required": True,
    },
    "type": {
        "type": "string",
        "required": True,
        "empty": False,
        "allowed": ["all", "any", "atLeast"],
        "dependencies": "name"
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
        "dependencies": "name"
    },
    "type_time": {
        "type": "string",
        "required": False,
        "empty": False,
        "allowed": ["before", "after"],
        "dependencies": ["name", "slot"]
    },
    "slot": {
        "type": "integer",
        "required": False,
        "empty": False,
        "dependencies": ["name", "type_time"]
    },
    "purpose": {
        "type": "string",
        "required": True,
        "allowed": ["mint", "multisig", "plutus"],
        "dependencies": "name"
    }
}