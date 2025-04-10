
create_user_responses = {
    201: {
        "content": {
            "application/json": {
                "example":{
                    "status": "ok",
                    "status_code": 201,
                    "data": None
                }
            }
        }
    },
    400: {
        "content": {
            "application/json": {
                "example":{
                    "status": "fail",
                    "status_code": 400,
                    "data": {"email": "Email already in use."}
                }
            }
        }
    }
}

update_user_responses = {
    200: {
        "content": {
            "application/json": {
                "example":{
                    "status": "ok",
                    "status_code": 200,
                    "data": None
                }
            }
        }
    },
    404: {
        "content": {
            "application/json": {
                "example":{
                    "status": "fail",
                    "status_code": 404,
                    "data": {"email": "User not found."}
                }
            }
        }
    }
}
