import os
import sys
import shutil

# python3 -m venv mturquin
# source mturquin/bin/activate

def is_in_venv() -> bool:
    return sys.prefix != sys.base_prefix

if __name__ == '__main__':
    if not is_in_venv():
        raise RuntimeError('Virtual enviroment is not running!')
    print(os.environ['VIRTUAL_ENV'])
    try:
        if not os.environ['VIRTUAL_ENV'].endswith('mturquin'):
            raise Exception('Incorrect env')
    except Exception as ex:
        print(ex)
    finally:
        try:
            os.system('pip install beautifulsoup4 PyTest termgraph')
            os.system('pip freeze > requirements.txt')
            shutil.make_archive("mturquin", "zip", 'mturquin')
        except RuntimeError as err:
            print(f'Runtime error: {err.args[0]}')
        # try:
        #     path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'mturquin')
        #     shutil.rmtree(path)
        # except RuntimeError as err:
        #     print(f'Delete error.')

# deactivate


