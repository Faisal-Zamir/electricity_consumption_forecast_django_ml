from django.shortcuts import render
import pandas as pd
from datetime import datetime
from consumption_predictor.ML_Files.energy_consumption_forecast import forecast_power
from consumption_predictor.forms import EnergyForecastForm
from django.http import JsonResponse  # add this at the top with imports

def homepage(request):
    df_predictions = None  # default
    forecast_json = None   # chart-ready JSON
    form = EnergyForecastForm()

    if request.method == "POST":
        form = EnergyForecastForm(request.POST)
        if form.is_valid():
            # Extract form data
            data = {
                "Global_reactive_power": [form.cleaned_data['current_power']],
                "Voltage": [form.cleaned_data['voltage']],
                "Global_intensity": [form.cleaned_data['global_intensity']],
                "Sub_metering_1": [form.cleaned_data['sub_metering1']],
                "Sub_metering_2": [form.cleaned_data['sub_metering2']],
                "Sub_metering_3": [form.cleaned_data['sub_metering3']],
                "timestamp": [form.cleaned_data['prediction_datetime']]
            }

            df_input = pd.DataFrame(data)
            minutes = int(form.cleaned_data['minutes_ahead'])

            # Call your model function (returns DataFrame)
            df_predictions = forecast_power(df_input, minutes_ahead=minutes)
            print(df_predictions)
            # Ensure your df_predictions contains time/power columns
            # Example expected output: columns ['minute', 'predicted_power']
            forecast_json = df_predictions.to_json(orient='records')
            print(forecast_json)  # For debugging

            # NEW: if AJAX request, send JSON
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'forecast': df_predictions.to_dict(orient='records')
                })
            
        else:
            # Handle invalid form for AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Invalid form submission'}, status=400)
    context = {
        'form': form,
        'forecast_json': forecast_json,  # <-- send this for JS
        'df_predictions': df_predictions
    }
    return render(request, 'consumption_predictor/homepage.html', context)






