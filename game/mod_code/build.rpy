## Build configuration #########################################################
##
## This section controls how Ren'Py turns your project into distribution files.

init python:
    build.packages = []

    build.package(build.directory_name + "CrossPlat",'zip','windows linux mac renpy mod binary',description="Sinking Love - Cross Platform")

    build.package(build.directory_name + "Windows Exclusive",'zip','windows renpy mod binary',description="Sinking Love - Windows")
    build.package(build.directory_name + "Mac Exclusive",'zip','mac renpy mod binary',description="Sinking Love - Mac")
    build.package(build.directory_name + "Linux Exclusive",'zip','linux renpy mod binary',description="Sinking Love - Linux")

    try:
        build.renpy_patterns.remove(build.pattern_list([("renpy.py", "all")])[0])
    except:
        pass

    build.classify_renpy("renpy.py", 'renpy all')

    build.archive("scripts", 'mod')
    build.archive("mod_assets", 'mod')
    build.archive("mod_code", 'mod')

    # To classify packages for both pc and android, make sure to add all to it like so
    # Example: build.classify("game/**.pdf", "scripts all")
    build.classify("game/mod_assets/**", "mod_assets all")
    build.classify("game/mod_code/**", "mod_code all")
    build.classify("game/**.rpyc", "scripts all")
    build.classify("game/mod_scripts/**", "scripts all")

    build.classify("game/README.txt", None)
    build.classify("game/python-packages/**", "mod all")

    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)
    build.classify('**.rpy', None)
    build.classify('**.psd', None)
    build.classify('**.sublime-project', None)
    build.classify('**.sublime-workspace', None)
    build.classify('/music/*.*', None)
    build.classify('script-regex.txt', None)
    build.classify('/game/10', None)
    build.classify('/game/cache/*.*', None)
    build.classify('**.rpa',None)
    build.classify('README.html','mod all')

    # Set's README.html as documentation
    build.documentation('README.html')

    build.include_old_themes = False

    # Advanced Addons
    # This section is for advanced build classifications to your mod that
    # can be added to your mod. Note DDLC runs as normal and doesn't require this.
    # This is either for compatibility issues or added features.

    # Doki Doki Mod Manager metadata file
    build.classify('ddmm-mod.json','mod')