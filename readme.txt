instrikcja instalacji:

1. Katalog "Delta" umieścić w dowolnym miejscu na dysku 
2. Plik "deltaRobot.desktop" umieścić na pulicie 
3. Wewnątrz "DeltaRobot.desktop" zamienić ścieżkę (Własna_ścieżka) na tą w której znajduje się skrypt delta.py
	Exec=python3 Własna_ścieżka/delta.py
	Path=Własna_ścieżka
	Icon=Własna_ścieżka/deltaIcon.jpg
4. Dodać plik wykonywalny do ścieżki przez wpisanie w terminalu:
	$ cd Desktop
	$ chmod +x DeltaRobot.desktop
5. Instalacja bibliotek:
	$ sudo apt-get install python3-pyqt5
	$ sudo apt-get install pyqt5-dev-tools
	$ sudo apt-get install qttools5-dev-tools
	$ sudo apt-get install python3-numpy
	$ sudo apt-get install python-matplotlib
	$ sudo apt-get install python3-opengl
	$ w katalogu głównym: git clone https://github.com/ROBOTIS-GIT/DynamixelSDK
	$ $ cd ~/DynamixelSDK/python i następnie sudo python3 setup.py install
	$ sudo apt-get install matchbox-keyboard (klawiatura ekranowa)
6. Po uruchomieniu programu nalezy wpisać dane konstrukcyjne
