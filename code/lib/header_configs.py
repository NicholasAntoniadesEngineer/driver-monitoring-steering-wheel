"""
Header configurations for different data capture types
"""

DEVICE_HEADERS = {
    'ECG_5LEAD': {
        'columns': ['ECG_1', 'ECG_2', 'ECG_3', 'ECG_4', 'ECG_5', 'tstamp'],
        'metadata': {
            'description': 'ECG 5-Lead Recording',
            'device_type': '5-Lead ECG Device'
        }
    },
    'ECG_IMU': {
        'columns': ['ECG_LOD', 'ECG_1', 'ECG_2', 'A_X', 'A_Y', 'A_Z', 
                   'G_X', 'G_Y', 'G_Z', 'M_X', 'M_Y', 'M_Z', 'tstamp'],
        'metadata': {
            'description': 'ECG and IMU Recording',
            'device_type': 'ECG+IMU Combined Device'
        }
    },
    'ECG_GRIP': {
        'columns': ['ECG_1', 'GRIP_FORCE', 'tstamp'],
        'metadata': {
            'description': 'ECG and Grip Force Recording',
            'device_type': 'Steering Wheel ECG'
        }
    }
} 