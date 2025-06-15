import httpx
import time
import secrets
import threading
from typing import List, Optional
from colorama import Fore, Style


class TikTokChecker:
    def __init__(self, file_path: str, threads: int):
        self.file_path = file_path
        self.threads = threads

        self.valid = 0
        self.bad = 0
        self.might_be_banned = 0
        self.errors = 0
        self.checked = 0

        self.lock = threading.Lock()
        self.sessions_list = self._load_session_ids()
        self.total = len(self.sessions_list)

    def _load_session_ids(self) -> List[str]:
        with open(self.file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    def _chunkify(self, lst: List[str], n: int) -> List[List[str]]:
        return [lst[i::n] for i in range(n)]

    def check_api(self, sessionid: str, client: httpx.Client) -> Optional[dict]:
        try:
            did = int(
                bin(int(time.time()) + secrets.randbelow(1_000_000))[2:]
                + "00101101010100010100011000000110",
                2,
            )
            response = client.get(
                url=(
                    f"https://api31-normal-alisg.tiktokv.com/passport/account/info/v2/"
                    f"?aid=1233&sdk_version=1012000&refresh_num=11&version_code=30.0.0"
                    f"&language=en-SA&display_density=1284*2778&device_id={did}&channel=AppStore"
                    f"&click_banner=32&mcc_mnc=42001&show_limit=0&resolution=1284*2778"
                    f"&version_name=9.1.1&os=ios&update_version_code=91115"
                    f"&access=WIFI&carrier=stc&ac=WIFI&os_version=17.3"
                    f"&is_cold_start=0&reason=0&device_platform=iphone&device_brand=AppleInc."
                    f"&device_type=iPhone13,4"
                ),
                headers={
                    "accept-encoding": "gzip",
                    "cookie": f"sessionid={sessionid}",
                    "host": "api31-normal-alisg.tiktokv.com",
                    "user-agent": "Dart/3.4 (dart:io)"
                }
            )
            return response.json().get('data')
        except Exception:
            return None

    def process_result(self, line: str, response: Optional[dict]):
        with self.lock:
            self.checked += 1
            if response:
                if 'error_code' not in response:
                    username = response.get('username', '')
                    if username:
                        with open("Valids.txt", "a", encoding="utf-8") as f:
                            f.write(f"{username}:{line}\n")
                        self.valid += 1
                    else:
                        with open("MightBeBanned.txt", "a", encoding="utf-8") as f:
                            f.write(f"{line}\n")
                        self.might_be_banned += 1
                else:
                    with open("Bads.txt", "a", encoding="utf-8") as f:
                        f.write(f"{line}\n")
                    self.bad += 1
            else:
                with open("toCheckAgain[Error].txt", "a", encoding="utf-8") as f:
                    f.write(f"{line}\n")
                self.errors += 1

    def console(self):
        while True:
            with self.lock:
                remaining = self.total - self.checked
                print(
                    f"{Fore.GREEN}Valid: {self.valid:,} "
                    f"{Fore.RED}| Bad: {self.bad:,} "
                    f"{Fore.YELLOW}| Errors: {self.errors:,} "
                    f"{Fore.CYAN}| Remaining: {remaining:,} lines{Style.RESET_ALL}",
                    end="\r"
                )
                if self.checked >= self.total:
                    print()
                    break
            time.sleep(1)

    def worker(self, chunk: List[str]):
        with httpx.Client() as client:
            for line in chunk:
                parts = line.split(":")
                sessionid = parts[2] if len(parts) > 2 else ""
                response = self.check_api(sessionid, client)
                self.process_result(line, response)

    def run(self):
        chunks = self._chunkify(self.sessions_list, self.threads)

        console_thread = threading.Thread(target=self.console)
        console_thread.start()

        workers = [
            threading.Thread(target=self.worker, args=(chunk,))
            for chunk in chunks
        ]

        for t in workers:
            t.start()

        for t in workers:
            t.join()

        console_thread.join()
        input("Press Enter to exit...")


if __name__ == "__main__":
    path = input(f"{Style.BRIGHT}Enter accounts file path [e.g., sessions.txt]: {Style.RESET_ALL}")
    checker = TikTokChecker(file_path=path, threads=10)
    checker.run()
