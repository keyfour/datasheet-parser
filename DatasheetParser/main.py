#!/usr/bin/env python3
import pdfreader


class Args:

    def __init__(self, file = ""):
        self.file = file


def main(args: Args):
    print("Parsing", args.file)
    reader = pdfreader.PDFReader(args.file)
    print(reader.read())


if __name__ == "__main__":
    import argparse

    args = Args()
    argparse = argparse.ArgumentParser(description="Datasheet Parser")
    argparse.add_argument('-f', '--file', help='PDF file')
    argparse.parse_args(namespace=args)
    main(args)