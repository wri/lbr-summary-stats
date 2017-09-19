from layer_stats.tcloss_layer import TcLoss
from utilities import geojson_to_geostore

def main():

    #make request to count TCloss, update gs
    TcLoss().update_gs('Protected Areas')
    print "GS updated with TC loss data"

if __name__ == "__main__":
    main()
