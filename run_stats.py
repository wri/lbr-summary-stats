import argparse

from layer_stats.analysis import Analysis
from layer_stats.umd_layer import UmdLayer
from layer_stats.terrai_layer import TerraiLayer
from layer_stats.biomass_layer import BiomassLayer

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
        umd_stats = UmdLayer().update_gs('Protected Areas')

        #Get Terra I stats for Protected Areas
        #Todo: fix terrai api for geostore requests (e.g., f57027ebca24f1a91eca803392bd5e0d)
        #terrai_stats = TerraiLayer().update_gs('Protected Areas')

        #Get Biomass Stats
        biomass_stats = BiomassLayer().update_gs('Protected Areas')

        #combine ditionaries
        all_stats = Analysis().combine_stats(umd_stats, biomass_stats=biomass_stats)

        #update google spreadsheet with layer stats
        Analysis().update_sheet('Protected Areas', all_stats)

        print "GS updated with TC loss data"

    else:
        print "Argument not found"


if __name__ == "__main__":
    main()
