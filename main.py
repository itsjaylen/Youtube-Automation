import logging
import time

from tools.video import process_channel

if __name__ == "__main__":
    valid_links = ["https://www.youtube.com/c/", "https://www.youtube.com/channel/",
                   "https://www.youtube.com/feeds/videos.xml?channel_id="]
    while True:
        try:
            print("Running video processor...10 minute delay")
            with open("channels.txt", encoding="utf-8") as channels:
                for channel in channels:
                    for link in valid_links:
                        if channel.startswith(link):
                            try:
                                print(f"Processing {channel}")
                                process_channel(channel)
                            except Exception:
                                pass
                    else:
                        continue

            print("Sleeping for 1800 seconds...")
            time.sleep(1800)

        except KeyboardInterrupt:
            print("Ending Processor")
            exit(-1)
