from darts.models.forecasting.transformer_model import TransformerModel


def get_cpu_usage_forcast(n):
    model = TransformerModel(input_chunk_length=12, output_chunk_length=1)
    model_path = 'cost_wiz/forcasting/time_series_cpu_usage.pt'
    pred = model.load(path=model_path)
    return pred.predict(n=n)


def get_mem_usage_forcast(n):
    model = TransformerModel(input_chunk_length=12, output_chunk_length=1)
    model_path = 'cost_wiz/forcasting/time_series_mem_usage.pt'
    pred = model.load(path=model_path)
    return pred.predict(n=n)


print(get_cpu_usage_forcast(n=48))
