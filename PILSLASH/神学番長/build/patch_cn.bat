@echo off
title ��ѧ���L ��������

rem 2014.2.7    by kid	����1����==���ӡ�����
rem 2013.12.30  by kid	���԰桫Ԫ����ɶ���ó���


if not exist BOOTUP.DAT (
	echo δ�ҵ��ļ�!��ŵ�exe���ڵ�ͬĿ¼��!
	goto END
)

echo ����ԭ�ļ�
if not exist BOOTUP.DAT.org (
	ren BOOTUP.DAT BOOTUP.DAT.org
)
move /Y patch_cn\BOOTUP.DAT BOOTUP.DAT

echo Ӧ�ò���,��һ��ʱ��,�����ĵȺ�!
for /f "delims= " %%i in (list.txt) do (
if not exist DATA\%%i.dat.org (
	ren DATA\%%i.dat %%i.dat.org
)
echo Patch %%i.dat...
xdelta3.exe -f -d -s DATA\%%i.dat.org patch_cn\%%i.diff DATA\%%i.dat
IF %errorlevel% NEQ 0 (goto FAILED)
)
IF %errorlevel% NEQ 0 (goto FAILED)

echo. 
echo ����Ӧ�óɹ���
echo ��ʹ�� "��ѧ���L��ȫ��_cn.exe" ���к�����~
goto END

:FAILED
echo. 
echo ����Ӧ��ʧ�ܣ�����Ŀ¼��

:END
del xdelta3.exe
del list.txt
rd /S/Q patch_cn
pause
del patch_cn.bat
