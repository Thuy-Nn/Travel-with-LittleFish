FUNCTIONS = {
    'API': [{
        "name": "get_flights",
        "description": "Get flights information",
        "arguments": {
            "originLocationCode",
            "destinationLocationCode",
            "departureDate",
            "adults",
            "returnDate"
        },
        "required": ["originLocationCode", "destinationLocationCode", "departureDate"]
    }, {
        "name": "get_hotels",
        "description": "Get hotels information",
        "arguments": {
            "cityCode",
            "adults",
            "checkInDate",
            "checkOutDate"
        },
        "required": ["cityCode", "checkInDate", "checkOutDate"]
    }, {
        "name": "get_places",
        "description": "Get places information",
        "arguments": {
            "searchQuery",
            "category"
        },
        "required": ["searchQuery", "category"]
    }],
    'UTILS': [{
        "name": "analyze_by_criteria",
        "description": "Analyze the response according to the criteria defined by user",
        "arguments": {
            "sortBy",
            "sortOrder"
        },
        "required": ["sortBy"]
    }]
}
