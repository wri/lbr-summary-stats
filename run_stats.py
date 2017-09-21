import argparse

from layer_stats.analysis import Analysis
from layer_stats.tcloss_layer import TcLoss
from layer_stats.tcgain_layer import TcGain

def main():

    #parse command line arguments
    parser = argparse.ArgumentParser(description='Separate Liberia stats calculations in command line')
    parser.add_argument('--run', '-r', required=True, choices=['protected_areas',
                        'forest_management_conracts', 'community_forests'],
                        help='the update process to kick off')
    args = parser.parse_args()

    #make request to count TCloss, update gs
    if args.run == "protected_areas":

        #get tcloss stats for Protected Areas
        tcloss_stats = TcLoss().update_gs('Protected Areas')

        #get tcgain stats for Protected Areas
        tcgain_stats = TcGain().update_gs('Protected Areas')

        #combine ditionaries
        all_stats = Analysis().combine_stats(tcloss_stats, tcgain_stats)

        #update google spreadsheet with layer stats
        Analysis().update_sheet('Protected Areas', all_stats)

        print "GS updated with TC loss data"

    else:
        print "Argument not found"


if __name__ == "__main__":
    main()
