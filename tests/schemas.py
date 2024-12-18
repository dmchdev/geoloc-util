zipcode_response_schema = {
    "type": "array",
    "items": {
        "type" : "object",
        "properties" : {
            "zip" : {"type" : "string"},
            "name" : {"type" : "string"},
            "lat" : {"type" : "number"},
            "lon" : {"type" : "number"},
            "country" : {"type" : "string"}
            }
        }
    }

city_state_response_schema = {
    "type": "array",
    "items": {
        "type" : "object",
        "properties" : {
            "name" : {"type" : "string"},
            "lat" : {"type" : "number"},
            "lon" : {"type" : "number"},
            "country" : {"type" : "string"},
            "state" : {"type" : "string"}
            }
        }
    }

multiple_locations_schema = {
    "type": "array",
    "items": {
        "anyOf": [
            {
            "type" : "object",
            "properties" : {
                "name" : {"type" : "string"},
                "lat" : {"type" : "number"},
                "lon" : {"type" : "number"},
                "country" : {"type" : "string"},
                "state" : {"type" : "string"}
                }
            },
            {
            "type" : "object",
            "properties" : {
                "zip" : {"type" : "string"},
                "name" : {"type" : "string"},
                "lat" : {"type" : "number"},
                "lon" : {"type" : "number"},
                "country" : {"type" : "string"}
                }
            }
        ]
        }
    }