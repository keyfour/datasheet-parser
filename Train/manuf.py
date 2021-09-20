import argparse
from html.parser import HTMLParser
from transitions import Machine


class ManufParser(object):
    states = ['ul_starttag', 'li_starttag', 'a_starttag', 'data', 'li_endtag']

    def __init__(self):
        self.state = None
        self.machine = Machine(
            model=self, states=ManufParser.states, initial='ul_starttag')
        self.machine.add_transition(
            trigger='search_li', source='ul_starttag', dest='li_starttag')
        self.machine.add_transition(
            trigger='search_li', source='li_endtag', dest='li_starttag')
        self.machine.add_transition(
            trigger='search_a', source='li_starttag', dest='a_starttag')
        self.machine.add_transition(
            trigger='search_ul', source='a_starttag', dest='ul_starttag')
        self.machine.add_transition(
            trigger='search_ul', source='li_starttag', dest='ul_starttag')
        self.machine.add_transition(
            trigger='search_ul', source='li_endtag', dest='ul_starttag')
        self.machine.add_transition(
            trigger='search_ul', source='data', dest='ul_starttag')
        self.machine.add_transition(
            trigger='search_data', source='a_starttag', dest='data')
        self.machine.add_transition(
            trigger='search_liend', source='data', dest='li_endtag')


class ManufHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.machine = ManufParser()
        self.manufacturers = []

    def handle_starttag(self, tag, attrs):
        if self.machine.state == 'ul_starttag' and tag == 'ul' and len(attrs) > 0:
            if attrs[0][0] == 'class':
                cl_attr = "".join(attrs[0][1])
                if 'mfr-category-list-items' in cl_attr:
                    # print("Found class: {0}".format(cl_attr))
                    self.machine.search_li()
        elif self.machine.state == 'li_starttag' and tag == 'li':
            self.machine.search_a()
        elif self.machine.state == 'a_starttag' and tag == 'a':
            self.machine.search_data()

    def handle_endtag(self, tag):
        if self.machine.state == 'li_endtag' and tag == 'li':
            self.machine.search_li()
        elif self.machine.state != 'ul_starttag' and tag == 'ul':
            self.machine.search_ul()

    def handle_data(self, data):
        if self.machine.state == 'data':
            manuf = [name.strip() for name in data.split('/')]
            self.manufacturers.extend(m for m in manuf if m != '')


def read_html(path):
    parser = ManufHTMLParser()
    with open(path, "r") as f:
        html = f.read()
        parser.feed(html)
    # print(parser.manufacturers)
    return parser.manufacturers


def write_output(file, output):
    with open(file, "w") as f:
        f.write(",".join(name for name in output))


if __name__ == "__main__":
    argparse = argparse.ArgumentParser()
    argparse.add_argument("-f", "--file", required=True,
                          help="Path to HTML file")
    argparse.add_argument("-o", "--output", help="Output file")
    args = argparse.parse_args()
    manufacturers = read_html(args.file)
    if args.output:
        write_output(args.output, manufacturers)
