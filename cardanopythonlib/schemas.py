
schema = {
            "address_origin": {
                "type": "string",
                "required": True,
            },
            "address_destin": {
                "type": "list",
                "nullable": True,
                "schema": {
                    "type": "dict",
                    "schema": {
                        "address": {"type": "string", "required": True},
                        "amount": {"type": "integer"},
                        "tokens": {
                            "type": "list",
                            "nullable": True,
                            "schema": {
                                "type": "dict",
                                "schema": {
                                    "name": {"type": "string", "required": True},
                                    "amount": {"type": "integer", "required": True},
                                    "policyID": {"type": "string", "required": True},
                                },
                            },
                        },
                    },
                },
            },
            "change_address": {
                "type": "string",
                "required": True,
            },
            "metadata": {
                "type": "dict",
                "nullable": True,
            },
            "mint": {
                "type": "dict",
                "nullable": True,
                "schema": {
                    "policyID": {"type": "string", "required": True},
                    "policy_path": {"type": "string", "required": True},
                    "validity_interval": {
                        "type": "dict",
                        "schema": {
                            "type": {"type": "string", "required": True},
                            "slot": {"type": "integer", "required": True},
                        },
                        "nullable": True,
                    },
                    "tokens": {
                        "type": "list",
                        "schema": {
                            "type": "dict",
                            "schema": {
                                "name": {"type": "string", "required": True},
                                "amount": {"type": "integer", "required": True},
                            },
                        },
                    },
                },
            },
            "script_path": {
                "type": "string",
                "nullable": True,
            },
            "witness": {
                "type": "integer",
                "required": False,
            },
            "inline_datum":{
                "type": "dict",
                "nullable": True,
            } 
        }
        