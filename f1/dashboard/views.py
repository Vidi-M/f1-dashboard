import fastf1
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
        
        # Fastest Laps Card
        fastest_lap = session.laps.pick_fastest()
        # fastest_laps_list = [
        #     {
        #         'driver': lap['Driver'],
        #         'team': lap['Team'],
        #         'lap_time': str(lap['LapTime']),
        #         'speed': lap['Speed']
        #     } for lap in fastest_laps.iterlaps()
        # ]
        
        # # Tire Strategy Card
        # tire_strategies = session.laps.groupby('Driver')['Compound'].value_counts()
        # tire_strategy_list = [
        #     {
        #         'driver': driver,
        #         'compounds': dict(tire_strategies[driver])
        #     } for driver in tire_strategies.groupby().index
        # ]
        
        context = {
             'driver_standings': driver_standings_list,
        #     'fastest_laps': fastest_laps_list,
        #     'tire_strategies': tire_strategy_list,
             'race_name': f"{session.event.year} {session.event.name}"
        }
        
        return render(request, 'dashboard.html', context)
    
    except Exception as e:
        context = {
            'error': str(e)
        }
        return render(request, 'dashboard.html', context)