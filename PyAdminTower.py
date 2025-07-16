import os
import sys
import platform
import subprocess
import time

def print_banner():
    print("██████╗ ██╗   ██╗     █████╗ ██████╗ ███╗   ███╗██╗███╗   ██╗    ████████╗ ██████╗ ██╗    ██╗███████╗██████╗ ")
    print("██╔══██╗╚██╗ ██╔╝    ██╔══██╗██╔══██╗████╗ ████║██║████╗  ██║    ╚══██╔══╝██╔═══██╗██║    ██║██╔════╝██╔══██╗")
    print("██████╔╝ ╚████╔╝     ███████║██║  ██║██╔████╔██║██║██╔██╗ ██║       ██║   ██║   ██║██║ █╗ ██║█████╗  ██████╔╝")
    print("██╔═══╝   ╚██╔╝      ██╔══██║██║  ██║██║╚██╔╝██║██║██║╚██╗██║       ██║   ██║   ██║██║███╗██║██╔══╝  ██╔══██╗")
    print("██║        ██║       ██║  ██║██████╔╝██║ ╚═╝ ██║██║██║ ╚████║       ██║   ╚██████╔╝╚███╔███╔╝███████╗██║  ██║")
    print("╚═╝        ╚═╝       ╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝       ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝")
    print("                                                                                                             ")
    print("="*100)
    print("Welcome to PyAdminTower!")
    print()

def show_menu():
    print("Available Options:")
    print("="*40)
    print("1. Check python installations")
    print("2. Check active installation of python")
    print("3. Manage Libraries")
    print("4. Manage Pip")
    print("5. Exit")
    print("="*40)

def is_microsoft_store_python(path):
    # Returns True if the path is a Microsoft Store alias
    if not path:
        return False
    return 'WindowsApps' in path and path.lower().endswith(('python.exe', 'python3.exe'))

def truncate(s, width):
    return (s[:width-3] + '...') if len(s) > width else s

def check_python_installations():
    print("\nChecking for Python installations on this system...\n")
    found = False
    python_names = [
        "python", "python3", "python2", "py", "python3.11", "python3.10", "python3.9", "python3.8", "python3.7", "python3.6", "python2.7"
    ]
    checked = set()
    results = []
    import shutil
    for name in python_names:
        if name in checked:
            continue
        checked.add(name)
        path = shutil.which(name)
        ms_store = is_microsoft_store_python(path)
        if path:
            found = True
            try:
                version = subprocess.check_output([path, "--version"], stderr=subprocess.STDOUT, text=True).strip()
            except Exception as e:
                version = f"Unknown version ({str(e).strip()})"
            results.append((version, name, path, ms_store))
    possible_dirs = [
        "/usr/bin", "/usr/local/bin", "/opt/python", "/opt/local/bin", "/bin", "/usr/sbin", "/sbin",
        os.path.expanduser("~/.pyenv/versions"),
        os.path.expanduser("~/.local/bin"),
        "C:/Python27", "C:/Python36", "C:/Python37", "C:/Python38", "C:/Python39", "C:/Python310", "C:/Python311"
    ]
    for d in possible_dirs:
        if os.path.isdir(d):
            for fname in os.listdir(d):
                if fname.startswith("python") and os.access(os.path.join(d, fname), os.X_OK):
                    full_path = os.path.join(d, fname)
                    if full_path in checked:
                        continue
                    checked.add(full_path)
                    ms_store = is_microsoft_store_python(full_path)
                    try:
                        version = subprocess.check_output([full_path, "--version"], stderr=subprocess.STDOUT, text=True).strip()
                    except Exception as e:
                        version = f"Unknown version ({str(e).strip()})"
                    results.append((version, fname, full_path, ms_store))
                    found = True
    if found:
        # Fixed column widths
        version_w = 20
        name_w = 10
        path_w = 60
        source_w = 22
        print(f"{'Version':<{version_w}} {'Name':<{name_w}} {'Path':<{path_w}} {'Source':<{source_w}}")
        print("-" * (version_w + name_w + path_w + source_w + 3))
        for version, name, path, ms_store in results:
            label = "Microsoft Store alias" if ms_store else ""
            print(f"{truncate(version, version_w):<{version_w}} {truncate(name, name_w):<{name_w}} {truncate(path, path_w):<{path_w}} {truncate(label, source_w):<{source_w}}")
    else:
        print("No Python installations found.")
    print()

def check_active_python():
    print("\nChecking active/default Python installation...\n")
    import shutil
    import subprocess
    python_path = shutil.which("python")
    ms_store = is_microsoft_store_python(python_path)
    if python_path:
        try:
            version = subprocess.check_output([python_path, "--version"], stderr=subprocess.STDOUT, text=True).strip()
        except Exception as e:
            version = f"Unknown version ({str(e).strip()})"
        label = " (Microsoft Store alias)" if ms_store else ""
        print(f"Default python executable: {python_path}{label}")
        print(f"Version: {version}")
    else:
        print("No default 'python' executable found in PATH.")
    print()

def manage_libraries():
    print("\nManaging libraries for all Python installations...\n")
    python_names = [
        "python", "python3", "python2", "py", "python3.11", "python3.10", "python3.9", "python3.8", "python3.7", "python3.6", "python2.7"
    ]
    checked = set()
    import shutil
    import subprocess
    import os
    all_libs = []  # (id, python_path, python_version, package, version)
    id_counter = 1
    for name in python_names:
        if name in checked:
            continue
        checked.add(name)
        path = shutil.which(name)
        if path:
            try:
                py_version = subprocess.check_output([path, "--version"], stderr=subprocess.STDOUT, text=True).strip()
            except Exception:
                py_version = "Unknown version"
            try:
                result = subprocess.run([path, "-m", "pip", "list", "--format=columns"], capture_output=True, text=True, timeout=20)
                if result.returncode == 0:
                    lines = result.stdout.strip().splitlines()
                    if len(lines) > 2:
                        for line in lines[2:]:
                            parts = line.split()
                            if len(parts) >= 2:
                                all_libs.append((id_counter, path, py_version, parts[0], parts[1]))
                                id_counter += 1
            except Exception:
                continue
    if not all_libs:
        print("No Python libraries found for any detected installation.")
        print()
        return
    # Print nicely formatted table
    print(f"{'ID':<4} {'Python Version':<18} {'Library':<30} {'Lib Version':<15} {'Python Path'}")
    print("-"*90)
    for lib in all_libs:
        idnum, py_path, py_version, pkg, pkgver = lib
        print(f"{idnum:<4} {py_version:<18} {pkg:<30} {pkgver:<15} {py_path}")
    print("\nOptions:")
    print("1. Remove library")
    print("2. Back to main menu")
    while True:
        choice = input("Enter your choice (1-2): ").strip()
        if choice == '1':
            try:
                lib_id = int(input("Enter the ID of the library to remove: ").strip())
            except ValueError:
                print("Invalid ID. Please enter a number.")
                continue
            match = next((lib for lib in all_libs if lib[0] == lib_id), None)
            if not match:
                print("No library found with that ID.")
                continue
            _, py_path, py_version, pkg, pkgver = match
            print(f"Uninstalling {pkg} from Python ({py_version}) at {py_path} ...")
            try:
                result = subprocess.run([py_path, "-m", "pip", "uninstall", pkg, "-y"], capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    print(f"Successfully uninstalled {pkg} from {py_path}")
                else:
                    print(f"Failed to uninstall {pkg}: {result.stderr}")
            except Exception as e:
                print(f"Error uninstalling: {e}")
            input("\nPress Enter to continue...")
            break
        elif choice == '2':
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

def manage_pip():
    print("\nManaging pip for all Python installations...\n")
    python_names = [
        "python", "python3", "python2", "py", "python3.11", "python3.10", "python3.9", "python3.8", "python3.7", "python3.6", "python2.7"
    ]
    checked = set()
    import shutil
    import subprocess
    import os
    import re
    import urllib.request
    import json
    all_pips = []  # (id, python_path, python_version, pip_version, pip_version_str, ms_store)
    id_counter = 1
    for name in python_names:
        if name in checked:
            continue
        checked.add(name)
        path = shutil.which(name)
        ms_store = is_microsoft_store_python(path)
        if path:
            try:
                py_version = subprocess.check_output([path, "--version"], stderr=subprocess.STDOUT, text=True).strip()
            except Exception:
                py_version = "Unknown version"
            try:
                result = subprocess.run([path, "-m", "pip", "--version"], capture_output=True, text=True, timeout=20)
                if result.returncode == 0:
                    pip_version_str = result.stdout.strip()
                    m = re.search(r'pip (\d+\.\d+(?:\.\d+)?)', pip_version_str)
                    pip_version = m.group(1) if m else None
                else:
                    pip_version_str = "pip not installed"
                    pip_version = None
            except Exception:
                pip_version_str = "pip not installed"
                pip_version = None
            all_pips.append((id_counter, path, py_version, pip_version_str, pip_version, ms_store))
            id_counter += 1
    if not all_pips:
        print("No pip installations found for any detected Python installation.")
        print()
        return
    # Fixed column widths
    id_w = 4
    pyver_w = 20
    pipver_w = 40
    path_w = 60
    source_w = 22
    print(f"{'ID':<{id_w}} {'Python Version':<{pyver_w}} {'Pip Version':<{pipver_w}} {'Python Path':<{path_w}} {'Source':<{source_w}}")
    print("-" * (id_w + pyver_w + pipver_w + path_w + source_w + 4))
    for pipinfo in all_pips:
        idnum, py_path, py_version, pipver_str, _, ms_store = pipinfo
        label = "Microsoft Store alias" if ms_store else ""
        print(f"{str(idnum):<{id_w}} {truncate(py_version, pyver_w):<{pyver_w}} {truncate(pipver_str, pipver_w):<{pipver_w}} {truncate(py_path, path_w):<{path_w}} {truncate(label, source_w):<{source_w}}")
    print("\nOptions:")
    print("1. Check All PIPs for updates")
    print("2. Update All PIPs")
    print("3. Update specific PIP")
    print("4. Back to main menu")
    while True:
        choice = input("Enter your choice (1-4): ").strip()
        if choice == '1':
            print("\nChecking for pip updates...")
            try:
                with urllib.request.urlopen("https://pypi.org/pypi/pip/json") as response:
                    pip_info = json.load(response)
                    latest_pip_version = pip_info['info']['version']
            except Exception as e:
                print(f"Could not fetch latest pip version from PyPI: {e}")
                latest_pip_version = None
            for idnum, py_path, py_version, pipver_str, pipver, ms_store in all_pips:
                if not pipver:
                    print(f"ID {idnum}: pip not installed in {py_path}")
                    continue
                if latest_pip_version:
                    if pipver != latest_pip_version:
                        print(f"ID {idnum}: Update available for pip in {py_path} (Installed: {pipver}, Latest: {latest_pip_version})")
                    else:
                        print(f"ID {idnum}: pip is up to date in {py_path} (Version: {pipver})")
                else:
                    print(f"ID {idnum}: Could not determine latest pip version.")
            print()
            break
        elif choice == '2':
            print("\nUpdating all pip installations...")
            for idnum, py_path, py_version, pipver_str, pipver, ms_store in all_pips:
                print(f"Updating pip for Python at {py_path}...")
                try:
                    result = subprocess.run([py_path, "-m", "pip", "install", "--upgrade", "pip"], capture_output=True, text=True, timeout=60)
                    if result.returncode == 0:
                        print(f"ID {idnum}: pip updated successfully.")
                    else:
                        print(f"ID {idnum}: pip update failed: {result.stderr}")
                except Exception as e:
                    print(f"ID {idnum}: Error updating pip: {e}")
            print()
            break
        elif choice == '3':
            try:
                pip_id = int(input("Enter the ID of the pip to update: ").strip())
            except ValueError:
                print("Invalid ID. Please enter a number.")
                continue
            match = next((pipinfo for pipinfo in all_pips if pipinfo[0] == pip_id), None)
            if not match:
                print("No pip found with that ID.")
                continue
            idnum, py_path, py_version, pipver_str, pipver, ms_store = match
            print(f"Updating pip for Python at {py_path}...")
            try:
                result = subprocess.run([py_path, "-m", "pip", "install", "--upgrade", "pip"], capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    print(f"ID {idnum}: pip updated successfully.")
                else:
                    print(f"ID {idnum}: pip update failed: {result.stderr}")
            except Exception as e:
                print(f"ID {idnum}: Error updating pip: {e}")
            print()
            break
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")



def main():
    while True:
        print_banner()
        show_menu()
        try:
            choice = input("Enter your choice (1-5): ").strip()
            if choice == '1':
                check_python_installations()
                input("\nPress Enter to continue...")
                os.system('cls' if platform.system() == "Windows" else 'clear')
            elif choice == '2':
                check_active_python()
                input("\nPress Enter to continue...")
                os.system('cls' if platform.system() == "Windows" else 'clear')
            elif choice == '3':
                manage_libraries()
                input("\nPress Enter to continue...")
                os.system('cls' if platform.system() == "Windows" else 'clear')
            elif choice == '4':
                manage_pip()
                input("\nPress Enter to continue...")
                os.system('cls' if platform.system() == "Windows" else 'clear')
            elif choice == '5':
                print("Thank you for using PyAdminTower!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")
                time.sleep(2)
                os.system('cls' if platform.system() == "Windows" else 'clear')
        except KeyboardInterrupt:
            print("\nThank you for using PyAdminTower!")
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            time.sleep(2)
            os.system('cls' if platform.system() == "Windows" else 'clear')

if __name__ == "__main__":
    import shutil
    main() 