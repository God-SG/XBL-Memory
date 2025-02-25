import sys, time, psutil, ctypes, ctypes.wintypes, subprocess, asyncio, aiohttp, pyperclip, os

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Ensure SIZE_T is defined
if not hasattr(ctypes.wintypes, 'SIZE_T'):
    ctypes.wintypes.SIZE_T = ctypes.c_size_t

# Windows API constants and setup
kernel32 = ctypes.windll.kernel32
PROCESS_ALL_ACCESS = 0x1F0FFF

# Structures for VirtualQueryEx and system info
class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BaseAddress",      ctypes.c_void_p),
        ("AllocationBase",   ctypes.c_void_p),
        ("AllocationProtect", ctypes.c_ulong),
        ("RegionSize",       ctypes.c_size_t),
        ("State",            ctypes.c_ulong),
        ("Protect",          ctypes.c_ulong),
        ("Type",             ctypes.c_ulong)
    ]

class SYSTEM_INFO(ctypes.Structure):
    _fields_ = [
        ("wProcessorArchitecture", ctypes.c_ushort),
        ("wReserved",              ctypes.c_ushort),
        ("dwPageSize",             ctypes.c_ulong),
        ("lpMinimumApplicationAddress", ctypes.c_void_p),
        ("lpMaximumApplicationAddress", ctypes.c_void_p),
        ("dwActiveProcessorMask",  ctypes.POINTER(ctypes.c_ulong)),
        ("dwNumberOfProcessors",   ctypes.c_ulong),
        ("dwProcessorType",        ctypes.c_ulong),
        ("dwAllocationGranularity", ctypes.c_ulong),
        ("wProcessorLevel",        ctypes.c_ushort),
        ("wProcessorRevision",     ctypes.c_ushort)
    ]

def get_system_info():
    sys_info = SYSTEM_INFO()
    kernel32.GetSystemInfo(ctypes.byref(sys_info))
    return sys_info

kernel32.VirtualQueryEx.restype = ctypes.c_size_t
kernel32.VirtualQueryEx.argtypes = [
    ctypes.c_void_p,
    ctypes.c_void_p,
    ctypes.POINTER(MEMORY_BASIC_INFORMATION),
    ctypes.c_size_t
]

kernel32.ReadProcessMemory.argtypes = [
    ctypes.c_void_p,
    ctypes.c_void_p,
    ctypes.c_void_p,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_size_t)
]
kernel32.ReadProcessMemory.restype = ctypes.c_bool

def open_process(pid):
    handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    return handle if handle else None

# Process management
def get_proc_id_by_name(name):
    for proc in psutil.process_iter():
        try:
            if proc.name().lower() == name.lower():
                return proc.pid
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None

def kill_xbox_apps():
    for proc in psutil.process_iter():
        try:
            if 'xbox' in proc.name().lower():
                print(f"{CYAN} Terminating {proc.name()} (PID {proc.pid}){RESET}")
                proc.kill()
        except Exception as e:
            print(f"{RED} Error terminating process: {e}{RESET}")

def start_xbox_app():
    try:
        subprocess.Popen(
            ["powershell.exe", "-Command", "Start-Process xbox://"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"{MAGENTA} Started Xbox app.{RESET}")
    except Exception as e:
        print(f"{RED} Error starting Xbox app: {e}{RESET}")

# Memory scanning
def scan_for_token(handle, pattern=b"XBL3.0 x="):
    sys_info = get_system_info()
    start_addr = (sys_info.lpMinimumApplicationAddress if isinstance(sys_info.lpMinimumApplicationAddress, int)
                  else sys_info.lpMinimumApplicationAddress.value)
    max_addr = (sys_info.lpMaximumApplicationAddress if isinstance(sys_info.lpMaximumApplicationAddress, int)
                else sys_info.lpMaximumApplicationAddress.value)
    addr = start_addr
    found_tokens = []
    mbi = MEMORY_BASIC_INFORMATION()
    while addr < max_addr:
        if kernel32.VirtualQueryEx(handle, ctypes.c_void_p(addr), ctypes.byref(mbi), ctypes.sizeof(mbi)):
            if mbi.State == 0x1000:  # MEM_COMMIT
                buffer = (ctypes.c_char * mbi.RegionSize)()
                bytes_read = ctypes.c_size_t(0)
                if kernel32.ReadProcessMemory(handle, ctypes.c_void_p(addr), buffer, mbi.RegionSize, ctypes.byref(bytes_read)):
                    data = bytes(buffer[:bytes_read.value])
                    index = data.find(pattern)
                    if index != -1:
                        read_len = min(10000, len(data) - index)
                        token_bytes = data[index:index+read_len].split(b'\0')[0]
                        try:
                            token = token_bytes.decode('utf-8')
                        except UnicodeDecodeError:
                            token = token_bytes.decode('latin1', errors='ignore')
                        found_tokens.append(token)
            addr += mbi.RegionSize
        else:
            break
    return found_tokens

def get_token(handle):
    tokens = scan_for_token(handle)
    if not tokens:
        return None
    frequency = {}
    for token in tokens:
        frequency[token] = frequency.get(token, 0) + 1
    most_common = max(frequency, key=frequency.get)
    return most_common if frequency[most_common] >= 3 else None

# Token validation using async HTTP request
async def validate_token(token):
    url = 'https://profile.xboxlive.com/users/me/profile/settings'
    headers = {
        'Authorization': token,
        'X-XBL-Contract-Version': '2',
        'Accept-Language': 'en-US',
        'Connection': 'keep-alive'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return response.status in [200, 201, 202, 204]

def get_save_path():
    current_directory = os.getcwd()
    return os.path.join(current_directory, 'xbl_token.txt')

def main():
    while True:
        print(f"{YELLOW} Terminating all Xbox processes... {RESET}")
        kill_xbox_apps()
        print(f"{GREEN} Launching a fresh Xbox app...{RESET}")
        start_xbox_app()

        print(f"{YELLOW} Scanning for token every 5 seconds for up to 90 seconds...{RESET}")
        scanning_duration = 90  # seconds
        scan_interval = 5       # seconds
        token = None
        start_time = time.time()

        while time.time() - start_time < scanning_duration:
            pid = get_proc_id_by_name("XboxPcApp.exe")
            if pid:
                print(f"{CYAN} Found XboxPcApp.exe (PID {pid}). Scanning memory...{RESET}")
                handle = open_process(pid)
                if handle:
                    token = get_token(handle)
                    if token:
                        # Validate the token asynchronously
                        is_valid = asyncio.run(validate_token(token))
                        if is_valid:
                            print(f"{GREEN} XBL Token: Has been found and is valid.{RESET}")
                            pyperclip.copy(token)
                            try:
                                file_path = get_save_path()
                                with open(file_path, "w") as f:
                                    f.write(token)

                                input(f"{MAGENTA} Token saved to 'xbl_token.txt' and copied to clipboard.\n{YELLOW} Press any key to close....{RESET}")
                            except Exception as e:
                                print(f"{RED} Error saving token: {e}{RESET}")
                            return
                        else:
                            print(f"{CYAN} Token is invalid. Continuing scan...{RESET}")
                    else:
                        print(f"{MAGENTA} No token found in this scan. Retrying in 5 seconds...{RESET}")
                else:
                    print(f"{YELLOW} Unable to open process. Retrying in 5 seconds...{RESET}")
            else:
                print(f"{GREEN} XboxPcApp.exe not found. Retrying in 5 seconds...{RESET}")
            time.sleep(scan_interval)
        
        print(f"{CYAN} No valid token found within 90 seconds. Restarting cycle...{RESET}\n")
        kill_xbox_apps()

if __name__ == "__main__":
    reaper = f"""{MAGENTA}
                  ...                            
                 ;::::;                           
               ;::::; :;                          
             ;:::::'   :;                         
            ;:::::;     ;.                        
           ,:::::'       ;           OOO\         
           ::::::;       ;          OOOOO\        
           ;:::::;       ;         OOOOOOOO       
          ,;::::::;     ;'         / OOOOOOO      
        ;:::::::::`. ,,,;.        /  / DOOOOOO    
      .';:::::::::::::::::;,     /  /     DOOOO   
     ,::::::;::::::;;;;::::;,   /  /        DOOO  
    ;`::::::`'::::::;;;::::: ,#/  /          DOOO 
    :`:::::::`;::::::;;::: ;::#  /            DOOO
    ::`:::::::`;:::::::: ;::::# /              DOO
    `:`:::::::`;:::::: ;::::::#/               DOO
     :::`:::::::`;; ;:::::::::##                OO
     ::::`:::::::`;::::::::;:::#                OO
     `:::::`::::::::::::;'`:;::#                O 
      `:::::`::::::::;' /  / `:#                  
       ::::::`:::::;'  /  /   `#      
 """
    print(reaper)
    main()
