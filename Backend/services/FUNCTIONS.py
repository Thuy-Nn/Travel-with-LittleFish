FUNCTIONS = {
    'API': [{
        "name": "get_flights",
        "description": "Get flights information",
        "parameters": {
            "type": "object",
            "properties": {
                "originLocationCode": {
                    "type": "string",
                    "description": "city/airport IATA code from which the traveler will depart, e.g. BOS for Boston"
                },
                "destinationLocationCode": {
                    "type": "string",
                    "description": "city/airport IATA code to which the traveler is going, e.g. PAR for Paris"
                },
                "departureDate": {
                    "type": "string",
                    "description": "the date on which the traveler will depart from the origin to go to the destination. Dates are specified in the ISO 8601 YYYY-MM-DD format, e.g. 2017-12-25"
                },
                "adults": {
                    "type": "string",
                    "description": "the number of adult travelers (age 12 or older on date of departure).The total number of seated travelers (adult and children) can not exceed 9."
                },
                "returnDate": {
                    "type": "string",
                    "description": "Dates are specified in the ISO 8601 YYYY-MM-DD format, e.g. 2018-02-28"
                }
            }
        },
        "required": ["originLocationCode", "destinationLocationCode", "departureDate"]
    }, {
        "name": "get_hotels",
        "description": "Get hotels information",
        "parameters": {
            "type": "object",
            "properties": {
                "cityCode": {
                    "type": "string",
                    "description": "Destination city code or airport code. In case of city code , the search will be done around the city center. Available codes can be found in IATA table codes (3 chars IATA Code)."
                },
                "adults": {
                    "type": "integer",
                    "description": "Number of adult guests (1-9) per room."
                },
                "checkInDate": {
                    "type": "string",
                    "description": "Check-in date of the stay (hotel local date). Format YYYY-MM-DD. The lowest accepted value is the present date (no dates in the past)."
                },
                "checkOutDate": {
                    "type": "string",
                    "description": "Check-out date of the stay (hotel local date). Format YYYY-MM-DD. The lowest accepted value is checkInDate+1."
                }
            }
        },
        "required": ["cityCode", "checkInDate", "checkOutDate"]
    }, {
        "name": "get_places",
        "description": "Get places information",
        "parameters": {
            "type": "object",
            "properties": {
                "searchQuery": {
                    "type": "string",
                    "description": "Text to use for searching based on the name of the location"
                },
                "category": {
                    "type": "string",
                    "description": "Filters result set based on property type. Valid options are 'attractions' or 'restaurants'"
                }
            }
        },
        "required": ["searchQuery", "category"]
    }],
    'UTILS': [{
        "name": "analyze_by_criteria",
        "description": "Analyze the response according to the criteria defined by user",
        "parameters": {
            "type": "object",
            "properties": {
                "content_type": {
                    "type": "string",
                    "description": "Specifies the type of requested content. Valid options are 'flights', 'hotels', 'attractions', or 'restaurants'."
                },
                "sort_by": {
                    "type": "string",
                    "description": "Specifies the criterion for sorting items in the list. Valid options are 'price', 'duration', 'rating', 'distance', or 'best_value'."
                },
                "sort_order": {
                    "type": "string",
                    "description": "Determines the sorting direction, which can either be 'ascending' or 'descending'."
                },
                "limit": {
                    "type": "integer",
                    "description": "The maximum number of items to be returned. Default is 10."
                }
            }
        },
        "required": ["content_type", "sortBy"]
    }]
}
