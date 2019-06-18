# ppGCS

stands for Parrot Python Ground Control Software
-

ok ok guys it's not another sexyiest Free Flight Pro clone

to be clear it's the uglyiest GCS you have ever seen (if you are god of python, QT, gstreamer,  and / or PySide2 you and your pull requests are more than welcome)

the objective is to be more easy plateform for seveal test purpose 
and first be able to control the drone on linux 

install 
-
it's intended to work on python3 variant 

you need zeroconf pygame and pyside2

  ``` pip3 install zeroconf PySide2 pygame```
  
clone this repo 
  
  ``` git clone https://github.com/profff/ppGCS.git ```

add submodules
  
  ```cd ppGCS; git submodule init; git submodule update```
  
  ```cd bybop; git submodule init; git submodule update```

install vlc and libvlc

  ```sudo apt install vlc libvlc-dev```

OpenSSl

it looks QT dont like last openssl release you have to downgrade to at least 1.0.2 to get map support
procedure is a bit tedious but trust me game is worth it!

follow this tutorial : https://www.howtoforge.com/tutorial/how-to-install-openssl-from-source-on-linux/
and it's ok


this is in perputual developpement so if it dont fit's your needs be patient or be active !!!!! ;)   

launch
-
```./ppGCS.py```
when started be sure to be connected to your parrot device via wifi or anything else (for exemple : zerotier if using uavpal 4g mod)
clic search device button
5 sec later your device must appear in left pannel just clic on it you are good to go ! 
