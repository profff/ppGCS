# ppGCS

stands for Parrot Python Ground Control Software
-

ok ok guys it's not another sexyiest Free Flight Pro clone

to be clear it's the uglyiest GCS you have ever seen (if you are god of QT and / or PySide2 your contributions are more than welcome)

the objective is to be more easy plateform for seveal test purpose 
and first be able to control the drone on linux 

install 
-
it's intended to work on python3 variant 

you need zeroconf pygame and pyside2

  ``` pip3 install zeroconf PySide2```
  
  ``` python3 -m pip install -U pygame --user```

clone this repo 
  
  ``` git clone https://github.com/profff/ppGCS.git ```

add submodules
  
  ```cd ppGCS/bybop; git submodule init; git submodule update```
  
  ```cd ppGCS/bybop/arsdk-xml/; git submodule init; git submodule update```
  
