import platform

keyboard_keys = {
    'Windows': {
        'up': 273,
        'down': 274,
        'right': 275,
        'left': 276,
        'space': 32,
    },
    'Darwin': {
        'up': 1073741905,
        'down': 1073741906,
        'right': 1073741903,
        'left': 1073741904,
        'space': 32,
    },
}

current_system = platform.system()
current_keys = keyboard_keys[current_system]