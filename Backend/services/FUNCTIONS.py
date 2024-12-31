FUNCTIONS = [{
    "name": "get_flight",
    "description": "Get flight information",
    "arguments": {
        "originLocationCode",
        "destinationLocationCode",
        "departureDate",
        "adults",
        "returnDate",
        "travelClass",
        "nonStop",
        "currencyCode"

    },
    "required": ["originLocationCode", "destinationLocationCode", "departureDate"]
},
    {
        "name": "get_hotels",
        "description": "Get hotel information",
        "arguments": {
            "cityCode",
            "adults",
            "checkInDate",
            "checkOutDate"
        },
        "required": ["cityCode", "checkInDate", "checkOutDate"]
    }
]
