import argparse
import pandas as pd
import numpy as np
import re
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, metavar="<input file>",
                    required=True,
                    help="Filename of input, must be tab-separated")
parser.add_argument('-o', '--output', type=str, metavar="<output file>",
                    required=True,
                    help="Filename for PDF output")
parser.add_argument('-d', '--gateDepth', type=int, metavar='',
                    help="Depth of gates to leave in parameter labels")
parser.add_argument('-l', '--labels', nargs='*', type=str, metavar="",
                    help="Labels for individual samples, provided in \
                    same order as samples")
parser.add_argument('-g', '--groups', nargs='*', type=str, metavar="",
                    help="Grouping variable, samples will be grouped \
                    into sequential blocks")
parser.add_argument('--excel', type=str,
                    help="Output the final data table used for plotting as \
                    a .xls using the provided filename")
args = parser.parse_args()


# Function definitions


def importData(filename):
    # Load data table
    df = pd.read_table(filepath_or_buffer=filename,
                       encoding="mac_roman")
    # Remove last two rows (mean and stdev)
    df = df.drop(df.tail(2).index)
    return(df)


def addLabels(df, labels):
    rpt_num = len(df) / len(labels)
    if rpt_num % 1 != 0:
        raise ValueError("The number of labels does not divide evenly into \
                         the number of samples!")
    df.insert(1, "Label", np.tile(labels, int(rpt_num)))
    return(df)


def addGroups(df, groups):
    rpt_num = len(df) / len(groups)
    if rpt_num % 1 != 0:
        raise ValueError("The number of groups does not divide evenly into \
                         the number of samples!")
    df.insert(2, "Group", np.repeat(groups, int(rpt_num)))
    return(df)


def regexDepth(d):
    '''Generates a regex pattern to trim gating paths to a specified
    depth d.'''
    string = "[^\/]+$"  # Default pattern, depth 0
    unit = "[^\/]+\/"  # Incremental unit of depth to add to regex
    if d == 0:
        return(re.compile("\/(" + string + ")"))
    else:
        return(re.compile("\/(" + "".join(np.repeat(unit, d)) + string + ")"))


def trimColnameDepth(df, pattern=None):
    '''Trim column names according to a regex pattern.
    Returns the first match to the regex as a list of new column names.
    If no match, returns unaltered column name.'''
    trimmed = []
    if not pattern:  # Default pattern if none provided
        pattern = re.compile(r"\/([^\/]+\/[^\/]+$)")
    for c in df.columns:
        match = pattern.search(c)  # Look for a match to the pattern
        if match:
            trimmed.append(match.group(1))
        else:
            trimmed.append(c)
    return(trimmed)


# Need to update plotting function to handle single-factor designs

def makePlots(df, filename):
    '''Generate a multi-page PDF containing plots for all variables'''
    with PdfPages(filename) as pdf:
        ppp = 4  # Plots per page
        for i, var in enumerate(df.columns[3:]):
            if i % ppp == 0:
                fig = plt.figure(figsize=(11, 8.5), dpi=100)
                fig.subplots_adjust(hspace=0.3)
                ax = fig.add_subplot(2, 2, i % ppp + 1)
            else:
                ax = fig.add_subplot(2, 2, i % ppp + 1)
            sns.catplot(data=df, x="Group", y=var,
                        hue="Label", dodge=True, kind="bar",
                        linewidth=1.5, facecolor=(1, 0, 1, 0),
                        errcolor=".2", edgecolor="0.5",
                        errwidth=1.5,
                        capsize=0.2, ci="sd", ax=ax, legend=False)
            ax.legend()
            sns.swarmplot(data=df, x="Group", y=var,
                          hue="Label", dodge=True, s=8, ax=ax)
            ax.set_title(var)
            if (i + 1) % ppp == 0:
                pdf.savefig(fig)
                plt.close()
            else:
                plt.close()
        if (i + 1) % ppp != 0:
            pdf.savefig(fig)


if __name__ == '__main__':
    df = importData(args.input)
    if args.labels:
        df = addLabels(df, args.labels)
    if args.groups:
        df = addGroups(df, args.groups)
    if args.gateDepth:
        df.columns = trimColnameDepth(df, pattern=regexDepth(args.gateDepth))
    makePlots(df, args.output)
    if args.excel:
        df.to_excel(excel_writer=args.excel)
