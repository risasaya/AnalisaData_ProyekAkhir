# AnalisaData_ProyekAkhir
Dicoding Proyek Analisa Data - Bike Sharing

## Data Understanding
- instant: record index
- dteday : date
- season : season (1:springer, 2:summer, 3:fall, 4:winter)
- yr : year (0: 2011, 1:2012)
- mnth : month ( 1 to 12)
- hr : hour (0 to 23)
- holiday : weather day is holiday or not (extracted from http://dchr.dc.gov/page/holiday-schedule)
- weekday : day of the week
- workingday : if day is neither weekend nor holiday is 1, otherwise is 0.
+ weathersit : 
	- 1: Clear, Few clouds, Partly cloudy, Partly cloudy
	- 2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
	- 3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
	- 4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog
- temp : Normalized temperature in Celsius. The values are divided to 41 (max)
- atemp: Normalized feeling temperature in Celsius. The values are divided to 50 (max)
- hum: Normalized humidity. The values are divided to 100 (max)
- windspeed: Normalized wind speed. The values are divided to 67 (max)
- casual: count of casual users
- registered: count of registered users
- cnt: count of total rental bikes including both casual and registered

## Run Dashboard
1. Clone Repositor

```https://github.com/risasaya/AnalisaData_ProyekAkhir.git```

2. Install Library

```pip install numpy pandas matplotlib seaborn jupyter streamlit babel```

3. Run Streamlit

```streamlit run dashboard.py```


## Tautan Dashboard
[Bike-Sharing-Dashboard](https://risadicodingdashboard.streamlit.app/)

## Dashboard
![image](https://github.com/risasaya/AnalisaData_ProyekAkhir/assets/90852026/9a3b9a1e-e15e-436f-b36c-4fc6d60e2a40)
![image](https://github.com/risasaya/AnalisaData_ProyekAkhir/assets/90852026/2560745f-d4a9-4ab8-9cf7-730788e3d725)
![image](https://github.com/risasaya/AnalisaData_ProyekAkhir/assets/90852026/81bb35a2-dd49-4118-9789-85c2277982b8)
![image](https://github.com/risasaya/AnalisaData_ProyekAkhir/assets/90852026/a91481bd-70a2-452b-b5e5-dcceae986e33)
