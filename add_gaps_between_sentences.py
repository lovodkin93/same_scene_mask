import argparse
desc="add gaps between sentences in order to easily pass it to Tupa"


def main(args):
    input_path = args.filenames[0]
    output_path = args.outdir
    input_file = open(input_path, 'r')
    output_file = open(output_path, 'w')

    sentences = input_file.readlines()
    for sent in sentences:
        output_file.writelines(sent)
        output_file.writelines('\n')
        output_file.writelines('\n')
    input_file.close()
    output_file.close()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="")
    argparser.add_argument("filenames", nargs="+", help=desc)
    argparser.add_argument("-o", "--outdir", default=".", help="output (with gaps) file text path")
    main(argparser.parse_args())
