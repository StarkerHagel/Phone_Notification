import platform
import subprocess
from plyer import notification  
from win10toast import ToastNotifier

def notify(title, text):
  system = platform.system()
  print(system)

  if system == 'Darwin': #macOS
    subprocess.run(["osascript", "-e", f'display notification "{text}" with title "{title}"'])
  elif system == 'Linux': #linux
    subprocess.run(['notify-send', title, text])
  elif system == 'Windows': #windows
    try:
      toaster = ToastNotifier()
      toaster.show_toast(title, text, duration=5)
    except ImportError:
      notification.notify(title=title, message=text, timeout=10)
