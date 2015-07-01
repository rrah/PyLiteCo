C:\python34\python.exe setup.py py2exe
"D:\Program Files (x86)\NSIS\makensis.exe" pyliteco.nsi
C:\Python34\python.exe pyliteco\version.py --rc True > temp
<temp set /p ver=
move /y pyliteco-setup.exe "pyliteco-setup-%ver%.exe