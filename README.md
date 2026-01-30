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
