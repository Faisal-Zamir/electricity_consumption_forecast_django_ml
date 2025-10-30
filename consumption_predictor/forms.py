from django import forms

class EnergyForecastForm(forms.Form):
    current_power = forms.FloatField(
        label="Global Active Power (kW)",
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 4.216',
            'step': '0.001',
            'id': 'currentPower'
        })
    )
    
    voltage = forms.FloatField(
        label="Voltage (V)",
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 234.84',
            'step': '0.01',
            'id': 'voltage'
        })
    )

    global_intensity = forms.FloatField(
        label="Global Intensity (A)",
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 18.4',
            'step': '0.1',
            'id': 'globalIntensity'
        })
    )

    sub_metering1 = forms.FloatField(
        label="Kitchen (Wh)",
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 0.0',
            'step': '0.1',
            'id': 'subMetering1'
        })
    )

    sub_metering2 = forms.FloatField(
        label="Laundry (Wh)",
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 1.0',
            'step': '0.1',
            'id': 'subMetering2'
        })
    )

    sub_metering3 = forms.FloatField(
        label="AC/Heating (Wh)",
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 17.0',
            'step': '0.1',
            'id': 'subMetering3'
        })
    )

    prediction_datetime = forms.DateTimeField(
        label="Start Prediction From",
        required=True,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
            'id': 'predictionDateTime'
        })
    )

    minutes_ahead = forms.ChoiceField(
        label="Forecast Duration",
        choices=[(20, "20 minutes ahead"), (30, "30 minutes ahead"),
                 (60, "1 hour ahead"), (120, "2 hours ahead")],
        initial=30,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'minutesAhead'
        })
    )
