## Pause Menu Stats (pause_menu_core.rpy)
## --------------------------------------
## Contains class and styles used for the pause menu.

style stats_text is gui_text:
    font "mod_assets/gui/font/AnonymousPro/AnonymousPro-Regular.ttf"
    hinting False

define -2 stats = GameStats()

init -10 python:
    import time

    class GameStats(object):
        style = "stats_text"

        def __init__(self):
            self.start_time = time.time()

        def formatted_time_text(self, seconds):
            format_string = "{hours:.0f}:{minutes:.0f}:{seconds:02.0f}"

            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)

            return Text(format_string.format(hours=hours, minutes=minutes, seconds=seconds), style=self.style)

        def runtime_function(self, *args):
            return self.formatted_time_text(time.time() - self.start_time), 0.0

        #################################################################
        #- Displayables -------------------------------------------------
        #################################################################

        def Runtime(self):
            return DynamicDisplayable(self.runtime_function)

        def TotalProgress(self):
            seen = renpy.count_seen_dialogue_blocks()
            total = renpy.count_dialogue_blocks()
            percentage = float(seen) / float(total)
            return Text("{:.2%}".format(percentage), style="stats_text")

        def CurrentPlaying(self):
            track = Soundtrack.get_current_track("music")

            if track is not None:
                return Text(track.track_name, style=self.style)

            return Text("Nothing is being played.", style=self.style)
