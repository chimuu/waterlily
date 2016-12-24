json = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "customer_name": {
            "type": "string",
            "required": True
        },
        "mobile": {
            "type": "number",
            "minimum": 10,
            "maximum": 10,
            "required": True
        },
        "customer_address": {
            "type": "string",
            "required": True
        },
        "measurements": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "measurment_type": "string",
                    "note": "string",
                    "details": {
                        "type": "array",
                        "properties": {
                            "name": {"type": "string"},
                            "value": {"type": "string"},
                            "display": {"type": "string"}
                        }
                    }
                }
            }
        },
        "bill": {
            "type": "object",
            "properties": {
                "total_price": {"type": "number"},
                "note": {"type": "string"},
                "details": {
                    "type": "array",
                    "items":{
                        "type": "object",
                        "properties": {
                            "type": {"type": "string"},
                            "quantity": {"type": "number"},
                            "price": {"type": "number"}
                        }
                    }
                }
            }
        }
    }
}
