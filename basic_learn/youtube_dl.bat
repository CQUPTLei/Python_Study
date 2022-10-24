@echo off
::olor 02
::==========================目录设置========================
::默认下载目录
:default_save_dir
set default_dir=D:\Python_Study\File_Save\test
pushd %default_dir%
echo 默认保存路径是：%cd%
set /p mode=是否需要重新设置保存目录？(y/n)
if /i %mode%==y call :set_dir
if /i %mode%==n call :download
if /i not %mode%==y if /i not %mode%==n  echo 输入有误
echo.
call :default_save_dir


::==========================下载========================
::下载视频，不点击退出则可一直在上述文件夹下下载
:download
echo.
set /p url=请输入视频URL：
set url=%url:&=^^^&%
::打印可供下载的视频格式
youtube-dl -F %url%
if errorlevel 1 goto :download
echo.
set /p code=请输入视频格式(format)：
::开始下载
youtube-dl -f %code% %url%
goto :download


::::==========================手动设置目录========================
:set_dir
echo.
set /p dir=请输入保存路径：
set dir=%dir:/=\%
::保存并切换到该目录
pushd %dir%
::比较当前路径与前面输入的路径是否一致，%cd%表示当前的绝对路径
if /i not %dir%==%cd% goto :set_dir
echo 现在的下载目录为：%cd%

