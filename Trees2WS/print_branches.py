import os, sys
import click
import uproot
# check the contents of a file

@click.command()
@click.option('--file', default='tmp.root', help='Path to input workspace')
def print_branches(file):
    try:
        rootfile = uproot.open(file)['tagsDumper/trees']
    except():
        print('Error loading file!')
        return
    print('|tagsDumper')
    print('|   trees')
    varlist = rootfile.keys()
    for var in varlist:
        sys.stdout.write('|      %s\n'%var)
    
    return

if __name__=="__main__":
    print_branches()