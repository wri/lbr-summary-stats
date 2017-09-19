from layer_stats.tcloss_layer import TcLoss
from utilities import geojson_to_geostore
from utilities import google_sheet as gs

def main():

    #make request to count TCloss, update gs
    TcLoss().update_gs('Protected Areas')
    print "GS updated with TC loss data"

    #Download spreadsheet
    gs.download_spreadsheet('https://docs.google.com/spreadsheets/d/1uWL2xf7XNkRfqmfBeV-KtEKLky_4kVFA7dZIsBMjuB8/export?format=csv&id=1uWL2xf7XNkRfqmfBeV-KtEKLky_4kVFA7dZIsBMjuB8&gid=0')

if __name__ == "__main__":
    main()
