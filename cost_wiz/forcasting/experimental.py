import pandas as pd
from darts import TimeSeries
from darts.models import ExponentialSmoothing


df = pd.read_csv('AirPassengers.csv')

series = TimeSeries.from_dataframe(df, 'Month', '#Passengers')
