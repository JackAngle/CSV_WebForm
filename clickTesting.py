import click


@click.group()
def greet():
    pass


@greet.command()
@click.argument('name')  # add the name argument
def hello(**kwargs):
    print('Hello, {0}!'.format(kwargs['name']))


@greet.command()
def hello2():
    key_convert_type = click.prompt('Please select convert type for keys: \n '
                                    '0 - No convert'
                                    '1 - All uppercase'
                                    '2 - All lowercase', type=int)


@greet.command()
@click.argument('name')
def goodbye(**kwargs):
    print('Goodbye, {0}!'.format(kwargs['name']))


@greet.command()
@click.option('--key-convert', '-kc',
              type=click.Choice(['uppercase', 'lowercase', '0', '1', '2'],
                                case_sensitive=False))
@click.option('--value-convert', '-vc',
              type=click.Choice(['uppercase', 'lowercase', '0', '1', '2'],
                                case_sensitive=False))
def say(key_convert, value_convert):
    print(key_convert)
    print(value_convert)

if __name__ == '__main__':
    hello2()
