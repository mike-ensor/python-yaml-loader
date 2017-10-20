import yaml
import os.path
import sys
import re

class Loader(yaml.Loader):
    """YAML Loader with `!include` constructor."""

    def __init__(self, stream):

        yaml.add_constructor('!include', self.construct_include)

        """Initialise Loader."""

        try:
            self._root = os.path.split(stream.name)[0]
        except AttributeError:
            self._root = os.path.curdir

        super(Loader, self).__init__(stream)

    def construct_include(self, tag_suffix, node):
        """Include file referenced at node."""

        filename = os.path.abspath(os.path.join(
            self._root, self.construct_scalar(node)
        ))
        extension = os.path.splitext(filename)[1].lstrip('.')

        with open(filename, 'r') as f:
            if extension in ('yaml', 'yml'):
                return yaml.load(f, Loader)
            else:
                return ''.join(f.readlines())


#########################################

def getReplacedYamlFile(lines):

    localoutput = ''

    for line in lines:

        matchObj = re.search(r'[\s+]!include[\s+]([\w]+[\S]*[\.]yaml)', line, re.M | re.I)

        if matchObj:
            localoutput += addIncludedFile(getSpacesToIndentOnIncludedFile(line), matchObj.group(1))
        else:
            localoutput += line

    return localoutput


def addIncludedFile(indentSpaces, fileToInclude):
    """
    Add the included file reference by !include <filename> at the proper indenting of the included attribute
    :param line: String line containing
    :param localoutput:
    :param matchObj:
    :return:
    """
    output = ''

    for includedLine in getFileContents(fileToInclude):
        output += indentSpaces + includedLine

    return output


def getSpacesToIndentOnIncludedFile(line):
    spacesToIndent = ''
    matchGroup = re.match(r'([\s]*).*!include[\s+][\w]+[\S]*[\.]yaml', line)
    if matchGroup:
        spacesToIndent = matchGroup.group(1)
    return spacesToIndent


def getFileContents(fileName):
    with open(fileName, 'r') as file:
        # print(os.path.realpath(file))
        return file.readlines()


if __name__ == '__main__':
    if len(sys.argv) < 2: 
        print("Please provide an input YAML file")
        sys.exit(1)



    finalOutput = getReplacedYamlFile(getFileContents(sys.argv[1]))

    yamlOutput = ''
    myfiles = yaml.load_all(finalOutput, Loader)

    for file in myfiles:
        yamlOutput += yaml.dump(file, default_flow_style=False) + "---\n"

    yamlOutput = re.sub('---\n$', '', finalOutput)

    print(yamlOutput)

    # Define Outfile path.
    finalOutputPath = re.sub('\.', '_final.', sys.argv[1])

    # Output file.
    
    text_file = open(finalOutputPath, "w")
    text_file.write(finalOutput)
    text_file.close()