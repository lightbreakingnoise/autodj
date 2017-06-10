# AutoDJ
### written in python3

You need icecast, libmp3lame-dev libshout-dev and libopus-dev

in lameshouter opusdec and opusenc you must do
```
python3 setup.py build
sudo python3 setup.py install
```

convert your audio files to a special opus-base64-zlib format with
```
python3 audioconvert.py "audiofile"
```

now you can start radio with
```
python3 play-radio.py
```

it will stream songs folder to your icecast and every full hour
the news folder
