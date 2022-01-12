## Rich Presence (rich_presence.rpy)
## ---------------------------------
## Class used for Discord Rich Presence using the `discord_rpc` module.
## (https://pypi.org/project/discord-rpc.py/) 

default -2 discord_status = ""
define -2 old_status = ""

init -15 python:
    import discord_rpc, time

    class DiscordPresence(object):
        TOKEN = '759375778626142240'

        SMALL_IMG_KEY = 'icebreaker_logo'
        LARGE_IMG_KEY = 'sinkinglovelogo'

        SMALL_IMG_TEXT = "An Icebreaker Production."
        LARGE_IMG_TEXT = "This game is an unofficial fan game, unaffiliated with Team Salvato."

        STARTED_UP_TEXT = 'Just started up.'

        @staticmethod
        def ready_callback(current_user):
            print('Our user: {}'.format(current_user))

        @staticmethod
        def disconnected_callback(codeno, codemsg):
            print('Disconnected from Discord rich presence RPC. Code {}: {}'.format(
                codeno, codemsg
            ))

        @staticmethod
        def error_callback(errno, errmsg):
            print('An error occurred! Error {}: {}'.format(
                errno, errmsg
            ))

        def __init__(self):
            self.start = time.time()

            self.initialize_rpc()
            self.update_presence(self.STARTED_UP_TEXT)
            self.update_info()

        def set_callbacks(self):
            config.interact_callbacks.append(self.interact_callback)

        def interact_callback(self):
            status = ''

            if renpy.context()._menu:
                if renpy.get_screen("music_menu"):
                    status = "On the Music Menu"

                elif renpy.get_screen("save"):
                    status = "On the Save Menu"

                elif renpy.get_screen("load"):
                    status = "On the Load Menu"

                elif renpy.get_screen("preferences"):
                    status = "On the Settings Menu"

                elif renpy.get_screen("pause_menu"):
                    status = "On the Pause Menu"

                elif renpy.context()._main_menu:
                    status = "On the Main Menu"

                else:
                    status = "Paused"

            else:
                status = discord_status

            if status == store.old_status:
                return

            self.update_presence(status)
            self.update_info()
            store.old_status = status
            return

        def quit_callback(self):
            discord_rpc.shutdown()

        def initialize_rpc(self):
            callbacks = {
                'ready': self.ready_callback,
                'disconnected': self.disconnected_callback,
                'error': self.error_callback,
            }
            discord_rpc.initialize(self.TOKEN, callbacks=callbacks, log=False)

            self.update_info()
            self.update_presence(self.STARTED_UP_TEXT)
            self.update_info()

        def update_info(self):
            discord_rpc.update_connection()
            discord_rpc.run_callbacks()
            return

        def update_presence(self, status):
            discord_rpc.update_presence(
                **{
                    'details': status,
                    'start_timestamp': self.start,
                    'large_image_key': self.LARGE_IMG_KEY,
                    'small_image_key': self.SMALL_IMG_KEY,
                    'large_image_text': self.LARGE_IMG_TEXT,
                    'small_image_text': self.SMALL_IMG_TEXT,
                }
            )