workflowStates = [
    'powerOff',
    'idle',
    'inProgress',
    'inSaveProgress',
    'error'
]

workflowTransitions = [
    {'trigger': 'on', 'source': 'powerOff', 'dest': 'idle'},
    {'trigger': 'start', 'source': 'idle', 'dest': 'inProgress'},
    {'trigger': 'save', 'source': [
        'inProgress', 'inSaveProgress'], 'dest': '='},
    {'trigger': 'autosaveoff', 'source': 'inSaveProgress', 'dest': 'inProgress'},
    {'trigger': 'autosave', 'source': 'inSaveProgress', 'dest': 'inProgress'},
    {'trigger': 'autosaveon', 'source': 'inProgress', 'dest': 'inSaveProgress'},
    {'trigger': 'autosave', 'source': 'inProgress', 'dest': 'inSaveProgress'},
    {'trigger': 'finish', 'source': [
        'inProgress', 'inSaveProgress'], 'dest': 'idle'},
    {'trigger': 'off', 'source': 'idle', 'dest': 'powerOff'}
]
