# Source Code

## Data Processing
 - [Preliminary analysis](preliminary_analysis.ipynb) - exploratory analysis and data plots
 - [Data processing](data_processing.ipynb) - combines data from multiple sources into full dataset
 - [Music data](music_stats.ipynb) - collect music similarity data from the Spotify API
 - [Music similarity](music_similarity_calculator.ipynb) - compute similarity coefficients between countries based on Spotify data
 - [Capital distances (old)](compute_distance.py) - computes distances between pairs of capital cities
 - [Eurovision distances (old)](eurovision_distances.ipynb) - combines Eurovision votes data with the distances between capitals

 ## Clustering
 - All include analysis and plots
 - [Distance clustering](clustering_distance.ipynb) - analysis of votes and distance
 - [GDP clustering](clustering_gdp.ipynb) - analysis of votes and GDP
 - [Music tastes clustering](clustering_tastes.ipynb) - analysis of votes and music taste similarity

 ## Linear Regression
 - All files include correlation analysis, overall regression, countrywise regression, result plots, and diagnostic plots
 - [Total votes analysis](linear_regression.ipynb)
    - also includes median and heteroscedasticity tests
- [Televoting analysis](linear_regression_televotes.ipynb)
- [Jury votes analysis](linear_regression_jury_votes.ipynb)
- [Televoting analysis including religion data (old)](linear_regression_televotes_with_religion.ipynb)

 ## Linear Mixed Effects
 - [Linear effects model](linear_effects_model.ipynb) - all analysis and plots


 ## Legal Notice

This is a university project and may be copied without at least one authors explicit permission. 
The datasets may not be downloaded or copied.
This especially includes the WRP Religion dataset (Zeev Maoz and Errol A. Henderson. 2013. “The World Religion Dataset, 1945-2010: Logic, Estimates, and Trends.” International Interactions, 39: 265-291.)

