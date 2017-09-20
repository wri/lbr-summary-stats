import argparse

from layer_stats.tcloss_layer import TcLoss

def main():

    #parse command line arguments
    parser = argparse.ArgumentParser(description='Separate Liberia stats calculations in command line')
    parser.add_argument('--run', '-r', required=True, choices=['protected_areas',
                        'forest_management_conracts', 'community_forests'],
                        help='the update process to kick off')
    args = parser.parse_args()

    #make request to count TCloss, update gs
    if args.run == "protected_areas":
        TcLoss().update_gs('Protected Areas')
        print "GS updated with TC loss data"
    else:
        print "Argument not found"

if __name__ == "__main__":
    main()
