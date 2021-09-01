#!/usr/bin/env python3
from pdfreader import PDFReader
from dsparser import DatasheetParser


class Args:

    def __init__(self, file = ""):
        self.file = file


def main(args: Args):
    print("Parsing", args.file)
    reader = PDFReader(args.file)
    parser = DatasheetParser()
    parser.get_entities(reader.read())


if __name__ == "__main__":
    import argparse

    args = Args()
    argparse = argparse.ArgumentParser(description="Datasheet Parser")
    argparse.add_argument('-f', '--file', help='PDF file')
    argparse.parse_args(namespace=args)
    main(args)