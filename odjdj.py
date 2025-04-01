import os
import shutil
import subprocess
import ctypes

def is_admin():
    """Checks if the script is running with administrator privileges."""
    try:
        return ctypes.windll.shell.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Reruns the script with administrator privileges."""
    ctypes.windll.shell.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    exit()

if not is_admin():
    run_as_admin()

try:
    # Close processes
    subprocess.run(["taskkill", "/f", "/im", "newui.exe"], capture_output=True, check=False)
    subprocess.run(["taskkill", "/f", "/im", "oldui.exe"], capture_output=True, check=False)

    # Delete newui.exe and oldui.exe
    script_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        os.remove(os.path.join(script_dir, "newui.exe"))
    except FileNotFoundError:
        pass
    try:
        os.remove(os.path.join(script_dir, "oldui.exe"))
    except FileNotFoundError:
        pass

    # Delete config folders
    for root, dirs, files in os.walk(script_dir, topdown=False):
        for name in dirs:
            if name == "config":
                try:
                    shutil.rmtree(os.path.join(root, name))
                except Exception as e:
                    print(f"Error deleting config folder: {e}")

    # Delete files in Ellie's folder
    ellie_path = os.path.join(os.environ["USERPROFILE"], "Ellie my precious girl", "Nudes", "Fansigns")
    if os.path.exists(ellie_path):
        try:
            shutil.rmtree(ellie_path)
        except Exception as e:
            print(f"Error deleting Ellie's folder contents: {e}")

    # USN Journal
    subprocess.run(["net", "stop", "usnsvc"], capture_output=True, check=False)
    subprocess.run(["fsutil", "usn", "deletejournal", "/d", "C:"], capture_output=True, check=False)
    subprocess.run(["net", "start", "usnsvc"], capture_output=True, check=False)

    # USB Drive Logs (Very dangerous, use with caution)
    import winreg
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Enum\USBSTOR")
        i = 0
        while True:
            try:
                subkey_name = winreg.EnumKey(key, i)
                subkey = winreg.OpenKey(key, subkey_name)
                try:
                    friendly_name, _ = winreg.QueryValueEx(subkey, "FriendlyName")
                    if friendly_name:
                        wmic_output = subprocess.run(["wmic", "diskdrive", "where", "InterfaceType='USB'", "get", "DeviceID", "/value"], capture_output=True, text=True, check=False).stdout
                        for line in wmic_output.splitlines():
                            if "DeviceID" in line:
                                device_id = line.split("=")[1].strip()
                                parts = device_id.split("\\")
                                if len(parts) > 2:
                                    oem_part = parts[2].split("#")[0]
                                    try:
                                        os.remove(rf"C:\Windows\inf\oem{oem_part}.inf")
                                        shutil.rmtree(rf"C:\Windows\System32\DriverStore\FileRepository\oem{oem_part}.inf_amd64_neutral_*", ignore_errors=True)
                                    except Exception as e:
                                        print(f"Error deleting USB logs: {e}")

                except OSError:
                    pass #FriendlyName not found
                winreg.CloseKey(subkey)
            except OSError:
                break
            i += 1
        winreg.CloseKey(key)

    except Exception as e:
        print(f"Error accessing registry: {e}")

    # Prefetch
    prefetch_path = r"C:\Windows\Prefetch"
    if os.path.exists(prefetch_path):
        try:
            shutil.rmtree(prefetch_path, ignore_errors=True)
            os.makedirs(prefetch_path) #Recreate the directory, as windows will do it anyway.
        except Exception as e:
            print(f"Error clearing Prefetch: {e}")

    # Temp
    temp_path = os.environ["TEMP"]
    if os.path.exists(temp_path):
        try:
            shutil.rmtree(temp_path, ignore_errors=True)
            os.makedirs(temp_path) #Recreate the directory, as windows will do it anyway.
        except Exception as e:
            print(f"Error clearing Temp: {e}")

    # Recycle Bin
    subprocess.run(["powershell", "-Command", "Clear-RecycleBin -Force"], capture_output=True, check=False)

    # Self-delete
    import sys
    subprocess.run(["powershell", "-Command", f'Start-Sleep -Seconds 1; Remove-Item -Path "{sys.argv[0]}" -Force'], capture_output=True, check=False)

except Exception as e:
    print(f"An error occurred: {e}")
