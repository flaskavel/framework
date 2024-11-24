"""
This module registers the native commands specific to the Flaskavel Framework.
"""

# A list of native commands, each defined by its module and class name.
native_commands = [
    {
        'module': 'flaskavel.lab.beaker.console.commands.schedule_work',
        'class': 'ScheduleWork'
    },
    {
        'module': 'flaskavel.lab.beaker.console.commands.loops_run',
        'class': 'LoopsRun'
    },
    {
        'module': 'flaskavel.lab.beaker.console.commands.key_generate',
        'class': 'KeyGenerate'
    },
    {
        'module': 'flaskavel.lab.beaker.console.commands.cache_clear',
        'class': 'CacheClear'
    },
    {
        'module': 'flaskavel.lab.beaker.console.commands.serve',
        'class': 'Serve'
    },
    {
        'module': 'flaskavel.lab.beaker.console.commands.make_controller',
        'class': 'MakeController'
    },
    {
        'module': 'flaskavel.lab.beaker.console.commands.make_command',
        'class': 'MakeCommand'
    },
    {
        'module': 'flaskavel.lab.beaker.console.commands.make_middleware',
        'class': 'MakeMiddleware'
    }
]
