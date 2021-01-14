import os
import argparse
from tupa.config import Config
from ucca import convert
from xml.etree.ElementTree import fromstring, tostring

import flask_assets
import jinja2
import matplotlib
from flask import Flask, render_template, Response, request
from flask_compress import Compress
from ucca.convert import from_text, to_standard, from_standard
from webassets import Environment as AssetsEnvironment
from webassets.ext.jinja2 import AssetsExtension

from tupa.parse import Parser

matplotlib.use("Agg")

SCRIPT_DIR = os.path.dirname(__file__)

app = Flask(__name__)
assets = flask_assets.Environment()
assets.init_app(app)
assets_env = AssetsEnvironment("./static/", "/static")
jinja_environment = jinja2.Environment(
    autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(SCRIPT_DIR, "templates")),
    extensions=[AssetsExtension])
jinja_environment.assets_environment = assets_env
Compress(app)
#
app.parser = None
PARSER_MODEL = r"C:\Users\aviv\Dropbox\My PC (DESKTOP-L80CN5A)\Desktop\studies\for the thesis\winscp\Semantic-Structural-Decomposition-for-NMT\code\DSS_rules\models\bert_multilingual_layers_4_layers_pooling_weighted_align_sum" #os.getenv("PARSER_MODEL", os.path.join(SCRIPT_DIR, "..", "models/bert_multilingual_layers_4_layers_pooling_weighted_align_sum"))
def get_parser(config):
    if app.parser is None:
        print("Initializing parser...")
        print("PARSER_MODEL=" + PARSER_MODEL)
        app.parser = Parser(model_files=config.args.models[0], config=config)
    return app.parser

def parse(config):
    text_path = config.args.passages[0] #r'C:\Users\aviv\Dropbox\My PC (DESKTOP-L80CN5A)\Desktop\delete\not_segmented.txt'
    output_path = config.args.outdir + "/ucca_trees.txt" #r'C:\Users\aviv\Dropbox\My PC (DESKTOP-L80CN5A)\Desktop\studies\for the thesis\winscp\Semantic-Structural-Decomposition-for-NMT\code\DSS_rules\u_trees2.txt'
    output_path = r"{}".format(output_path)
    f_read = open(text_path, 'r')
    sentences = f_read.readlines()
    parser = get_parser(config)
    output_file = open(output_path, 'w')

    for i, sent in enumerate(sentences):
        sent_passage = next(from_text(sent, lang=config.args.lang))
        out_passage = next(parser.parse(sent_passage))[0]
        out_passage.attrib["lang"] = config.args.lang
        root = to_standard(out_passage)
        xml = tostring(root).decode()
        # to save (all in the same file)
        output_file.writelines(xml)
        output_file.writelines('\n')
        output_file.writelines('\n')


        # # to decode
        # from ucca import convert
        # xml_object1 = fromstring(xml)
        # P1 = convert.from_standard(xml_object1)

        # # to save
        # import os
        # xml_dir = "xmls"
        # if not os.path.isdir(f'{xml_dir}'):
        #     os.mkdir('xmls')
        # b = open(f"{xml_dir}/{i}.xml", "w")
        # b.write(xml)
        # b.close()
    f_read.close()
    output_file.close()
    print("done!")
    # check what was written - will save each line into a different xml (under "./xmls").
    input_file = open(output_path, 'r')
    sentences = input_file.readlines()
    for i, xml in enumerate(sentences):
        if xml == '\n':
            continue
        xml_dir = "xmls"
        if not os.path.isdir(f'{xml_dir}'):
            os.mkdir('xmls')
        b = open(f"{xml_dir}/{i}.xml", "w")
        b.write(xml)
        b.close()
    input_file.close()

def main(config):
    parse(config)

if __name__ == "__main__":
    desc = "receive a file where each line is one sentence, and UCCA-parse each sentence independently and save all the parsings into one file"
    # argparser = argparse.ArgumentParser(description="self-parsing")
    # argparser.add_argument("filenames", nargs="+", help=desc)
    # argparser.add_argument("-m", "--model", default=".", help="path to the parser model")
    # argparser.add_argument("-o", "--outdir", default=".", help="output file text path")
    # argparser.add_argument("-l", "--lang", default="en", help="small two-letter language code to use for NLP model")
    # argparser.add_argument("--bert-multilingual", choices=[0], type=int)
    # add_boolean_option(argparser, "use-bert", default=False, description="whether to use bert embeddings")
    config = Config()
    main(config)