from cx_Freeze import setup, Executable


options = {
    'build.exe': {
        'includes':[
            'runner',
            'table_builder'
        ]
    }
}

setup(
    name='Exchange_rate_parser',
    version='1.6',
    description='Simple parser and table builder.',
    options=options,
    executables=[Executable('table_builder.py')]
)