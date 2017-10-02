import argparse

from layer_stats.analysis import Analysis
from layer_stats.umd_layer import UmdLayer
from layer_stats.terrai_layer import TerraiLayer
from layer_stats.biomass_layer import BiomassLayer
from utilities import arcgis_online

def main():

    #parse command line arguments
    parser = argparse.ArgumentParser(description='Separate Liberia stats calculations in command line')
    parser.add_argument('--run', '-r', required=True, choices=['protected_areas',
                        'forest_management_contracts', 'community_forests'],
                        help='the update process to kick off')
    parser.add_argument('--features', '-f', required=False, help='Features in dataset to update')
    args = parser.parse_args()

    #make request to count TCloss, update gs
    if args.run == "protected_areas":

        #get tcloss stats for Protected Areas
        umd_stats = UmdLayer().update_gs('Protected Areas', features=args.features)

        # Get Biomass Stats
        biomass_stats = BiomassLayer().update_gs('Protected Areas', features=args.features)

        # update google spreadsheet with layer stats
        Analysis().update_sheet('Protected Areas', umd_stats)
        print "GS updated with TC loss data for Portected Areas"

        Analysis().update_sheet('Protected Areas', biomass_stats)
        print "GS Updated with Biomass data for Protected Areas"

        # Downlaod sheet_name
        Analysis().download_sheet('Protected Areas')

    elif args.run == 'forest_management_contracts':

        # get tcloss stats for Protected Areas
        umd_stats = UmdLayer().update_gs('Forest Management Contracts', features=args.features)

        # Get Biomass Stats
        biomass_stats = BiomassLayer().update_gs('Forest Management Contracts', features=args.features)

        #update google spreadsheet with layer stats
        Analysis().update_sheet('Forest Management Contracts', umd_stats)
        print "GS updated with TC loss data for Forest Management Contracts"

        Analysis().update_sheet('Forest Management Contracts', biomass_stats)
        print "GS Updated with Biomass data for Forest Management Contracts"

        #Downlaod sheet_name
        Analysis().download_sheet('Forest Management Contracts')

    elif args.run == 'community_forests':

        #get tcloss stats for Protected Areas
        umd_stats = UmdLayer().update_gs('Community Forests', features=args.features)

        #Get Biomass Stats
        biomass_stats = BiomassLayer().update_gs('Community Forests', features=args.features)

        #update google spreadsheet with layer stats
        Analysis().update_sheet('Community Forests', umd_stats)
        print "GS updated with TC loss data for Community Forests"

        Analysis().update_sheet('Community Forests', biomass_stats)
        print "GS Updated with Biomass data for Community Forests"

        #Downlaod sheet_name
        Analysis().download_sheet('Community Forests')

    else:
        print "Argument not found"


if __name__ == "__main__":
    main()
