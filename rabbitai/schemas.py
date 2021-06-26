from rabbitai.errors import RabbitaiErrorType

error_payload_content = {
    "application/json": {
        "schema": {
            "type": "object",
            "properties": {
                # SIP-40 error payload
                "errors": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "message": {"type": "string"},
                            "error_type": {
                                "type": "string",
                                "enum": [enum.value for enum in RabbitaiErrorType],
                            },
                            "level": {
                                "type": "string",
                                "enum": ["info", "warning", "error"],
                            },
                            "extra": {"type": "object"},
                        },
                    },
                },
                # Old-style message payload
                "message": {"type": "string"},
            },
        },
    },
}
"""错误载荷内容架构"""
