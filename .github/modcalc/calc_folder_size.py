import os, requests, subprocess

def du(path):
    return subprocess.check_output(['du','-sh', path]).split()[0].decode('utf-8')

if __name__ == "__main__":

    url = os.getenv("DISCORD_WEBHOOK")

    if url is None:
        quit()

    mod_assets_size = du("game/mod_assets")
    mod_code_size = du("game/mod_code")
    mod_scripts_size = du("game/mod_scripts")
    game_folder_size = du("game")
    message = (
        "```asciidoc\n"
        "Folders:\n"
        "-------\n"
        f"mod_assets :: {mod_assets_size}\n"
        f"mod_code :: {mod_code_size}\n"
        f"mod_scripts :: {mod_scripts_size}\n"
        f"game :: {game_folder_size}\n"
        "```"
    )

    values = {
        "title": "Doki Doki Sinking Love",
        "content": message
    }

    r = requests.post(url, json=values)
