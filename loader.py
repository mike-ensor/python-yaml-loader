import yaml
import os.path
import sys

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


if __name__ == '__main__':
    if len(sys.argv) < 2: 
        print("Please provide an input YAML file")
        sys.exit(1)

    finalList = []
    with open(sys.argv[1], 'r') as f:
        yamlSegments = yaml.load_all(f, Loader)
        for segment in yamlSegments:
            data = yaml.dump(segment)
            print data
            finalList.append(segment)
    print finalList