@echo off
::olor 02
::==========================Ŀ¼����========================
::Ĭ������Ŀ¼
:default_save_dir
set default_dir=D:\Python_Study\File_Save\test
pushd %default_dir%
echo Ĭ�ϱ���·���ǣ�%cd%
set /p mode=�Ƿ���Ҫ�������ñ���Ŀ¼��(y/n)
if /i %mode%==y call :set_dir
if /i %mode%==n call :download
if /i not %mode%==y if /i not %mode%==n  echo ��������
echo.
call :default_save_dir


::==========================����========================
::������Ƶ��������˳����һֱ�������ļ���������
:download
echo.
set /p url=��������ƵURL��
set url=%url:&=^^^&%
::��ӡ�ɹ����ص���Ƶ��ʽ
youtube-dl -F %url%
if errorlevel 1 goto :download
echo.
set /p code=��������Ƶ��ʽ(format)��
::��ʼ����
youtube-dl -f %code% %url%
goto :download


::::==========================�ֶ�����Ŀ¼========================
:set_dir
echo.
set /p dir=�����뱣��·����
set dir=%dir:/=\%
::���沢�л�����Ŀ¼
pushd %dir%
::�Ƚϵ�ǰ·����ǰ�������·���Ƿ�һ�£�%cd%��ʾ��ǰ�ľ���·��
if /i not %dir%==%cd% goto :set_dir
echo ���ڵ�����Ŀ¼Ϊ��%cd%

