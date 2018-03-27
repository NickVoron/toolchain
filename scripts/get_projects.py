import template
import shutil
import sys
import getopt

# return project list from package which input from param 'template-file'


def get_projects(template_file):
    tmpdir = template.gettempdir()
    for key, item in template.extractReplaceDictMetadata(template_file, tmpdir).items():
        print(key)
    shutil.rmtree(tmpdir)


def run():
    input_args = sys.argv[1:]  # skip first param - path to python file
    optlist, args = getopt.getopt(input_args, '', ['template-file='])

    template_file = ''
    for opt_type, value in optlist:
        if opt_type == "--template-file":
            template_file = value
            pass

    get_projects(template_file)


run()
