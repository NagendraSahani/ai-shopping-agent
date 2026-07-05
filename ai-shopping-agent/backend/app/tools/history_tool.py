import json
import os


class HistoryTool:

    FILE = "history.json"

    @staticmethod
    def load():

        if not os.path.exists(
            HistoryTool.FILE
        ):
            return []

        with open(
            HistoryTool.FILE,
            "r",
            encoding="utf8",
        ) as f:

            return json.load(f)

    @staticmethod
    def save(result):

        history = HistoryTool.load()

        history.append(result)

        history = history[-30:]

        with open(

            HistoryTool.FILE,

            "w",

            encoding="utf8",

        ) as f:

            json.dump(

                history,

                f,

                indent=4,

            )

    @staticmethod
    def get_last():

        history = HistoryTool.load()

        if len(history):

            return history[-1]

        return None