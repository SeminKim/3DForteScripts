import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# base_dir =os.getcwd()
base_dir = 'Directory Here'


class Target:
    watchDir = base_dir

    # watchDir에 감시하려는 디렉토리를 명시한다.

    def __init__(self):
        self.observer = Observer()  # observer객체를 만듦

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDir,
                               recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Error")
            self.observer.join()


class Handler(FileSystemEventHandler):
    # FileSystemEventHandler 클래스를 상속받음.
    # 아래 핸들러들을 오버라이드 함

    # 파일, 디렉터리가 move 되거나 rename 되면 실행
    def on_moved(self, event):
        return

    def on_created(self, event):  # 파일, 디렉터리가 생성되면 실행
        guid = event.src_path.replace(base_dir, "")[1:]
        print(guid)

    def on_deleted(self, event):  # 파일, 디렉터리가 삭제되면 실행
        return

    def on_modified(self, event):  # 파일, 디렉터리가 수정되면 실행
        return


if __name__ == '__main__':
    # 본 파일에서 실행될 때만 실행되도록 함
    w = Target()
    w.run()
