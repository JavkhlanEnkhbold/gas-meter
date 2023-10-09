# gas-meter
This is a small DIY gas-meter built with Raspberry Uno, a magnet sensor. Influxdb is installed in the Raspberry and later Grafan is being used for monitoring.
Once the this is being built, you can attach it in magnetic gas meters which can be found in typical european old buildings.
The project is being built during the "energy-crisis" in Germany, where the gas price on the Spot market more than tripled and to give the user more energy visibility of their own.

## Zum Testen
1. cd Desktop 
2. git clone https://github.com/JavkhlanEnkhbold/gas-meter.git
3. cd gas-meter 
4. cd monitoring (in RaspberryPi)
5. python gas_meter.py & python update_influx.py

### NOTE: BEIDE Python Scripts in dem selben Ordner "monitoring" kopieren!


## Zu neuen Features
1. cd Desktop git clone https://github.com/JavkhlanEnkhbold/gas-meter.git
2. git checkout -b new_branch_name
3. Code
4. git add .
5. git commit -m "ich habe das gemacht"
6. git push --set-upstream origin new_branch_name
