# Music-Assistant-Satelit

ESP HOME - HA - MA Satelit - MA Radio player

  - teljes értékü assist satelit + mediaplayer -  lokal wake word stb.
  - kezdőképen idő, hőmérséklet+páratartalom, és világítás kapcsoló HA megfelelő entitásokból
  - Music Assistant felől, kedvenc webrádiók leszedése (MA URL + Ikon) max 24db (python script állítja elő egy szenzorba + generálja az ikonokat HA oldalon - ESP csak feldolgozza,
    meg töltögeti a képeket)
  - kiválasztott rádió lejátszása (pause-start, stop) + hangerő fel-le + aktuális előadó + számcím kirakása (amennyiben van)
  - állapot ikonok dinamikusan változnak a felső sorban (HA kapcsolat, WW aktiv/passzív, player tipus)
  - kijelző fényerő, time out HA-ból állítható, tapizásra felébred:)

Base Assistant code from AshaiRey : 
https://github.com/AshaiRey/ESP-Assistant/blob/main/ESP%20Assistant%20v4.yaml

![Music Assistant Satelite](/Picture/pic1.jpg)

Hardver:
- ESP32S3 N16R8 Wroom-1
- MAX98375 speaker DAC
- INMP441  mic
- 2.8" 240x320 SPI TFT érintőképernyő (Ili9341 driverrel) SD kártya csatlakozó nincs használva
- 4W speaker

![Music Assistant Satelite](/SCHEMATIC/circuit_image.png)

1, Home Assistant oldali előkészületek:

icon_worker.py

Feladata a rádió ikonok előállítása és tárolása a /config/www/icons könyvtárba amit az ESP képes olvasni.
Az ikonok 64x64 méretre vannak normalizálva, jpg formátumra. Az icon_worker képes a nem négyzetes ikonoknak, vagy hiányzó ikonoknak egyszerü saját ikont generálni. Azért kerül külön modulba, hogy aszinkron hívható legyen - igy nem akasztja meg a HA működését. A scriptet a config/python_modules könyvtárba kell betenni (ha nincs elötte létre kell hozni) és utána teljes HA restart hogy a modul késöbbiekben használható legyen.

ma_get_radios.py

Feladata: olvassa a Music Assisstant könyvtárát és onnan kiszedi a kedvencnek beállított rádiókat. (max 24db képes kezelni)
A kiolvasott rádiók MA url-jét és a rádió ikon url-jét betárolja a sensor.radiok -ba (url, név, ikon url)
A függvényt minden HA restart, update, MA restart után kötelező meghívni különben az ESP nem kap adatot!




További bővítési lehetőségek: 
-  MA YT musik kedvencek kezelése, dinamikus ikonok megjelenítésével (folyamatban)
-  több képernyős kezdőoldal több HA entitással  
-  MAX98375 helyet 2db MAX98375A használatával stereo player

