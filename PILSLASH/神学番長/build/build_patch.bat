@echo off

set RAR="C:\Program Files\WinRAR\Rar.exe"
set PATCH="xdelta3.exe"
set ORGDIR="E:\��ѧ���L��ȫ��\Data"

for /f "delims= " %%i in (list.txt) do (
echo %%i
%PATCH% -9 -v -e -s %ORGDIR%\%%i.dat.org %%i.dat patch_cn\%%i.diff
)

copy /Y BOOTUP.DAT patch_cn\BOOTUP.DAT
%RAR% a patch.exe %PATCH%
%RAR% a patch.exe patch_cn\*
%RAR% a patch.exe "��ѧ���L��ȫ��_cn.exe"
%RAR% a patch.exe list.txt
%RAR% a patch.exe patch_cn.bat

del patch_cn\*.diff

pause
