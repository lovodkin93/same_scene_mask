import argparse
desc="seperate data into smaller groups"
# how to run: python3 seperate_data.py <source file> -o <target file> --min=<minimum index of the source file. default:0> --max=<maximum index of the source file. default:end of file>

def main(args):
    input_path = args.filenames[0]
    output_path = args.outdir
    input_file = open(input_path, 'r')
    output_file = open(output_path, 'w')


    sentences = input_file.readlines()
    min=int(args.min)
    max=len(sentences) if args.max==-1 else int(args.max)
    for sent in sentences[min:max]:
        output_file.writelines(sent)
    input_file.close()
    output_file.close()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="")
    argparser.add_argument("filenames", nargs="+", help=desc)
    argparser.add_argument("-o", "--outdir", default=".", help="output (with gaps) file text path")
    argparser.add_argument("--min", help="lower bound", default=0)
    argparser.add_argument("--max", help="upper bound", default=-1)


    main(argparser.parse_args())
