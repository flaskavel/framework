"""
This module registers the native commands specific to the Flaskavel framework.
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
    }
]
