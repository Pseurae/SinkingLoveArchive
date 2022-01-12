
init python:
    import re
    from vorbis import Vorbis

    _music_player_channel = "music_player"

    renpy.music.register_channel(_music_player_channel, mixer=_music_player_channel, tight=True)

    class Soundtrack(object):
        soundtracks = list()

        def __init__(self, track_name, artist_name, track_filepath, category=None):
            self.track_name = track_name
            self.artist_name = artist_name
            self.track_filepath = track_filepath
            self.category = category

            if self not in self.soundtracks:
                self.soundtracks.append(self)

        def __repr__(self):
            return "%s by %s" % (self.track_name, self.artist_name)

        def __unicode__(self):
            return "%s by %s" % (self.track_name, self.artist_name)

        @classmethod
        def get_current_track(cls, channel="music"):
            now_playing = renpy.music.get_playing(channel)

            if now_playing is None:
                return None

            now_playing = re.sub(r'^<.*?>', '', now_playing)

            for track in cls.soundtracks:
                if track.track_filepath == now_playing:
                    return track

            return None

        @classmethod
        def construct_soundtracks(cls):
            if cls.soundtracks:
                return

            for track_filepath in renpy.list_files():
                if "mod_assets/bgm" not in track_filepath:
                    continue

                comments = Vorbis(track_filepath).comments
                title = comments.get("title", "")
                artist = comments.get("artist", "")

                category = "Unsorted"

                for name in ("monika", "sayori", "yuri", "natsuki", "general"):
                    if name in track_filepath:
                        category = name
                        break

                cls(title, artist, track_filepath, category)

            cls.soundtracks = list(cls.soundtracks)

    config.start_callbacks.append(Soundtrack.construct_soundtracks)

screen music_menu(return_action=Return()):
    tag menu

    use game_menu("{music_note}  Music")