{
    "name": "VKoo - Appointments Calender Custom",
    "version": "1.0",
    "author": "VKoo",
    "category": "Services/Appointment",
    "sequence": 220,
    "summary": "",
    "website": "",
    "description": """
    """,
    "depends": [
        "appointment",
    ],
    "data": ["views/calendar_views.xml", "views/appointment_views.xml"],
    "installable": True,
    "application": False,
    'license': 'LGPL-3',
    "assets": {
        "web.assets_backend": [
            "/appointment_custom/static/src/views/**/*.js",
            "/appointment_custom/static/src/views/**/*.xml",
            "/appointment_custom/static/src/views/**/*.css",
        ],
    },
}
