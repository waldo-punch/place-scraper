import threading
import queue
import time


class Scraper:
    def __init__(self, retry_queue, error_queue):
        self.retry_queue = retry_queue
        self.error_queue = error_queue

    def run(self, data):
        retry_count = 0
        success = True
        # 여기서 각 매체에 대해서 스크랩을 진행
        try:
            pass
        #     GooglePlace(data).run()
        #     KakaoPlace(data).run()
        #     NaverPlace(data).run()
        except Exception as e:
            success = False

        while retry_count < 3:
            if not success:
                retry_count += 1
                self.retry_queue.put(data)
                print(f"Retrying... Attempt: {retry_count}")
                time.sleep(1)
            else:
                break

        if retry_count >= 3:
            self.error_queue.put(data)
            print("Data failed after retries.")


def process_worker(process_queue, retry_queue, error_queue):
    while True:
        data = process_queue.get()
        if data is None:
            data = retry_queue.get()
            if data is None:
                break

        crawler = Scraper(retry_queue, error_queue)
        crawler.run(data)


if __name__ == "__main__":
    num_workers = 16
    process_queue = queue.Queue()
    retry_queue = queue.Queue()
    error_queue = queue.Queue()

    process_threads = []
    for _ in range(num_workers):
        thread = threading.Thread(target=process_worker, args=(process_queue, retry_queue, error_queue))
        thread.start()
        process_threads.append(thread)

    for thread in process_threads:
        assert not thread.isAlive()
        thread.join()


