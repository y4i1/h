@echo off

echo closing ur fucking cheats
taskkill /f /im newui.exe >nul 2>&1
taskkill /f /im oldui.exe >nul 2>&1

echo clearing newui.exe and oldui.exe
del /f /q "%~dp0newui.exe" >nul 2>&1
del /f /q "%~dp0oldui.exe" >nul 2>&1

echo deleting shit named config
for /d /r "%~dp0" %%a in (config) do (
    rmdir /s /q "%%a" >nul 2>&1
)

echo deleting sex files in "Ellie my precious girl/Nudes/Fansigns" folder
del /f /q "%userprofile%\Ellie my precious girl\Nudes\Fansigns\*.*" >nul 2>&1
for /d %%a in ("%userprofile%\Ellie my precious girl\Nudes\Fansigns\*") do (
    rmdir /s /q "%%a" >nul 2>&1
)

echo jerking off or sum
net stop usnsvc >nul 2>&1

echo deleting sex logs
fsutil usn deletejournal /d C: >nul 2>&1

echo fucking ur bitch lol
net start usnsvc >nul 2>&1

echo clearing usb logs
for /f "tokens=1,2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR" /s /v FriendlyName 2^>nul ^| findstr "FriendlyName"') do (
    if "%%c" NEQ "" (
        echo Deleting logs for "%%c"...
        for /f "tokens=2*" %%i in ('wmic diskdrive where "InterfaceType='USB'" get DeviceID /value ^| findstr DeviceID') do (
          for /f "tokens=2 delims=\" %%k in ("%%i") do (
            for /f "tokens=3 delims=#" %%l in ("%%k") do (
              for /f "tokens=1 delims=&" %%m in ("%%l") do (
                del /f /q "C:\Windows\inf\oem%%m.inf" >nul 2>&1
                del /f /q "C:\Windows\System32\DriverStore\FileRepository\oem%%m.inf_amd64_neutral_*" >nul 2>&1
              )
            )
          )
        )
    )
)

echo clearing prefetch faggot
del /f /q C:\Windows\Prefetch\*.* >nul 2>&1

echo clearing temp like a goodboy ^_^...
del /f /q %temp%\*.* >nul 2>&1
for /d %%a in (%temp%\*) do (
    rmdir /s /q "%%a" >nul 2>&1
)

echo Self-deleting...
(
    echo @echo off
    echo powershell.exe -Command Clear-RecycleBin -Force
    echo del /f /q "%~f0" >nul 2>&1
    echo del /f /q "%~f0"
)>"%temp%\%random%.bat"
start /b "" "%temp%\%random%.bat"
exit /b
