# yadrif version-1.0.1
import pandas as pd

class Yadrif:
    def __init__(self):
        self.commands = {
            "time": self.get_time,
            "date": self.get_date,
            "hello": self.greet,
            "shutdown": self.shutdown,
            "music_info": self.get_music_info
        }

        self.music_df = pd.read_csv('ClassicHit.csv')

    def get_music_info(self):
        track_name = input("Enter the track name: ").title()
        if track_name in self.music_df['Track'].values:
            track_data = self.music_df[self.music_df['Track'] == track_name]
            return track_data
        else:
            return "Track not found."

    def get_time(self):
        now = datetime.datetime.now()
        return now.strftime("The current time is %H:%M")

    def get_date(self):
        today = datetime.date.today()
        return today.strftime("Today is %B %d, %Y")

    def greet(self):
        return "Hello! How can I assist you today?"

    def shutdown(self):
        return "Shutting down yadrif"

    def response(self, input_text):
        for command in self.commands:
            if command in input_text.lower():
                return self.commands[command]()
        return "Sorry, searching from online sources."

    def run(self):
        print("Activating yadrif services")
        while True:
            user_input = input("You: ")
            respond = self.response(user_input)
            print(f"Y.A.D.R.I.F: {respond}")
            if user_input.lower() == "shutdown":
                break

if __name__ == "__main__":
    assist = Yadrif()
    assist.run()
