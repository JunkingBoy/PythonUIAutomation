import sys
import os
import subprocess
import urllib.request


def check_or_download(file_name: str) -> None:
    python_installation_path: str = os.path.dirname(sys.executable)
    get_pip_path: str = os.path.join(python_installation_path, file_name)

    if os.path.exists(get_pip_path):
        # 执行python get-pip.py
        subprocess.run(["python", get_pip_path])
    else:
        try:
            # 下载get-pip.py文件
            url: str = "https://bootstrap.pypa.io/get-pip.py"
            urllib.request.urlretrieve(url, python_installation_path)
            if os.path.exists(get_pip_path):
                # 执行python get-pip.py
                subprocess.run(["python", get_pip_path])
        except Exception as e:
            print(f"Download and install error: {e}")

if __name__ == "__main__":
    check_or_download("get-pip.py")
