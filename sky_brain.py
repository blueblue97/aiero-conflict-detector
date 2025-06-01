def detect_conflicts(df):
    conflicts = []
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            if df.iloc[i]['time'] == df.iloc[j]['time']:
                dist_lat = abs(df.iloc[i]['latitude'] - df.iloc[j]['latitude'])
                dist_lon = abs(df.iloc[i]['longitude'] - df.iloc[j]['longitude'])
                dist_alt = abs(df.iloc[i]['altitude'] - df.iloc[j]['altitude'])
                if dist_lat < 1 and dist_lon < 1 and dist_alt < 1000:
                    conflicts.append({
                        "flight_id": df.iloc[i]['flight_id'],
                        "latitude": df.iloc[i]['latitude'],
                        "longitude": df.iloc[i]['longitude'],
                        "altitude": df.iloc[i]['altitude'],
                        "conflict_with": df.iloc[j]['flight_id']
                    })
    return conflicts
