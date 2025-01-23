from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import fastf1
import pandas as pd

def dashboard(request):
    try:
        # Load session details
        session = fastf1.get_session(2024, 'Baku', 'Race')
        session.load()
        
        # Get lap data
        lap_data = session.laps
        
        # Convert to a format easy to pass to template
        top_drivers = lap_data.groupby('Driver')[['LapTime']].min().sort_values('LapTime').head(10)
        
        # Convert Dataframe to a list of dictionaries for easier rendering
        driver_stats = [
            {
                'driver': index, 
                'best_lap_time': str(row['LapTime'])
            } for index, row in top_drivers.iterrows()
        ]
        
        context = {
            'driver_stats': driver_stats,
            'race_name': f"{session.event.year} {session.event.name}"
        }
        
        return render(request, 'dashboard.html', context)
    
    except Exception as e:
        # Handle any errors
        context = {
            'error': str(e)
        }
        return render(request, 'dashboard.html', context)
    
    # template = loader.get_template('dashboard.html')
    # return HttpResponse(template.render())
