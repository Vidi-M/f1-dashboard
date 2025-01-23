import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render

def dashboard(request):
    fastf1.Cache.enable_cache('cache/')
    
    try:
        # Fetch the most recent race weekend
        session = fastf1.get_session(2023, 'Abu Dhabi', 'Race')
        session.load()
        
        # Driver Standings Card
        driver_standings = session.results.iloc[:]
        driver_standings_list = [
            {
                'position': int(row['Position']),
                'grid': row['GridPosition'],
                'gain': int(row['Position'] - row['GridPosition']),
                'driver': row['Abbreviation'],
                'team': row['TeamName'],
                'interval': row['Time'],
                'points': int(row['Points'])
            } for _, row in driver_standings.iterrows()
        ]
        
        context = {
             'driver_standings': driver_standings_list,
             'race_name': f"{session.event['EventName']} {session.event.year}"
        }
        
        return render(request, 'dashboard.html', context)
    
    except Exception as e:
        context = {
            'error': str(e)
        }
        return render(request, 'dashboard.html', context)