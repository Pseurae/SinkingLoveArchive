init -1000 python:

    def modified_screenshot():
        import os.path
        import os
        import __main__

        dest = config.basedir

        if renpy.macapp:
            dest = os.path.expanduser(b"~/Desktop")

        # Try to pick a filename.
        i = 1
        while True:
            fn = os.path.join(dest, config.screenshot_pattern % i)
            if not os.path.exists(fn):
                break
            i += 1

        try:
            dn = os.path.dirname(fn)
            if not os.path.exists(dn):
                os.makedirs(dn)
        except:
            pass

        try:
            if not renpy.screenshot(fn):
                renpy.notify(__("Failed to save screenshot as %s.") % fn)
                return
        except:
            import traceback
            traceback.print_exc()
            renpy.notify(__("Failed to save screenshot as %s.") % fn)
            return

        if config.screenshot_callback is not None:
            config.screenshot_callback(fn)

    _default_keymap.keymap["screenshot"] = modified_screenshot