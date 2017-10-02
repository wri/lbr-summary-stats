# Liberia Forest Atlas Summary Stats

System to update Google Sheets with statistics created from intersecting data
features from the [Liberia Forest Atlas](http://lbr.forest-atlas.org) with forest
change data in the [Global Forest Watch](http://developers.globalforestwatch.org/)
API.

## Getting Started

lbr-summary-stats runs from the command line and uses keyword arguments to trigger
statistic calculations.

To create a table of forest change stats for the Protected Areas in Liberia:

`python run_stats.py -r protected_areas`

To create a table of forest change stats for the Forest Management Contracts in Liberia:

`python run_stats.py -r forest_management_contracts`

To create a table of forest change stats for the Community Forests in Liberia:

`python run_stats.py community_forests`

Optionally, use the -f argument to limit the analyses for a particular feature in each dataset.
Set the feature argument to string.

e.g,
`python run_stats.py -r forest_management_contracts -f "Lake Piso"`

## Available analyses

The GFW analyses currently available for Liberia include:

Dataset | Description
--- | ---
Tree cover loss | Identifies areas of gross tree cover loss (2001-2015)
Tree cover gain | Identifies areas of tree cover gain (2000-2012)
Terra I Alerts | Detects areas where tree cover loss is likely to have recently occurred (2000-2016)
Active Fires | Identifies location of fire hotspots for the past week
Aboveground live woody biomass density | Shows carbon density values of aboveground live woody biomass across the tropics.
