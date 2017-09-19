from layer_stats.tcloss_layer import TcLoss
from utilities import geojson_to_geostore

def main():

    #get layer_dict
    layer_dict = geojson_to_geostore.create_geostore_dict('Protected Areas')

    #make request to count TCloss and update layer_dict
    layer_stats = TcLoss().count_tcloss(layer_dict, 'umd-loss-gain')

    print layer_stats
    # return layer_stats

if __name__ == "__main__":
    main()
