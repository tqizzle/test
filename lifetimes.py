import lifetimes
from lifetimes import BetaGeoFitter
from lifetimes.plotting import plot_frequency_recency_matrix
from lifetimes.plotting import plot_probability_alive_matrix

import pandas as pd

data = pd.read_csv('lifetimes')


bgf = BetaGeoFitter(penalizer_coef=0.0)
bgf.fit(data['frequency'], data['recency'], data['T'])

print bgf

plot_frequency_recency_matrix(bgf)

#plot_probability_alive_matrix(bgf)
