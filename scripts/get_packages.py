import template
import ntpath

# return package list


def get_templates():
    result = []

    absfolder = ntpath.abspath('toolchain/wizard')
    # absfolder = ntpath.abspath('../wizard')
    for file in template.get_files(absfolder, 'zip'):
        result.append(file)
    return result


for templateFile in get_templates():
    print(templateFile)




