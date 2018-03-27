# script for creation of a new project from ProjectWizard
import sys
import getopt
import template


def create():
    input_args = sys.argv[1:]   # skip first param - path to python file
    optlist, args = getopt.getopt(input_args, '', ['package=', 'project=', 'module=', 'name='])

    package = ''
    project = ''
    module = ''
    new_project_name = ''

    for opt_type, value in optlist:
        if opt_type == "--package":
            package = value
            pass
        if opt_type == "--project":
            project = value
            pass
        if opt_type == "--module":
            module = value
            pass
        if opt_type == "--name":
            new_project_name = value
            pass
        pass

    # print('package:{0}, project:{1}, module:{2}, name:{3}'.format(package, project, module, new_project_name))

    template.unpack_project(package, module, project, new_project_name);
    pass


if __name__ == '__main__':
    create()
