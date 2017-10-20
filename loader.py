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


def getReplacedYamlFile(lines):
    localoutput  = ""

    for l in lines:
        line = l

        matchObj = re.search(r'[\s+]!include[\s+]([\w]+[\.]yaml)', line, re.M | re.I)

        if matchObj:
            fileToInclude = matchObj.group(1)
            includedFileLines = getFileContents(fileToInclude)
            for includedLine in includedFileLines:
                localoutput += includedLine
        else:
            localoutput += line


    print(localoutput)
    return localoutput


def getFileContents(fileName):
    with open(fileName, 'r') as file:
        return file.readlines()


if __name__ == '__main__':
    if len(sys.argv) < 2: 
        print("Please provide an input YAML file")
        sys.exit(1)

    finalOutput = ''
    # myfiles = yaml.load_all(f, Loader)
    # for file in myfiles:
    #     finalOutput += yaml.dump(file, default_flow_style=False) + "---\n"
    newYamlFile = getReplacedYamlFile(getFileContents(sys.argv[1]))
    print(newYamlFile)

    # Remove last ---
    
    finalOutput = re.sub('---\n$', '', finalOutput)
    
    # Define Outfile path.
    
    finalOutputPath = re.sub('\.', '_final.', sys.argv[1])
    
    # Output file.
    
    text_file = open(finalOutputPath, "w")
    text_file.write(finalOutput)
    text_file.close()