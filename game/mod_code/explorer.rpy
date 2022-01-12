## Explorer (explorer.rpy)
## -----------------------
## In game explorer that lets you choose the vanilla DDLC zip and extracts it, if the
## `.rpa` files are missing.

init python in explorer_icons:
    from store.icon_res import nf_icon, fi_icon
    from renpy.config import self_closing_custom_text_tags

    self_closing_custom_text_tags["upper_level"] = fi_icon("")
    self_closing_custom_text_tags["file"] = fi_icon("")
    self_closing_custom_text_tags["folder"] = fi_icon("")
    self_closing_custom_text_tags["folder_connect"] = nf_icon("")

init python:
    import os, zipfile

    ddlc_win_zip_hash = "09a4e1bf2ab801908b3199f901bd8b0d"
    ddlc_mac_zip_hash = "dddd082cd9e51c6cfdecbbcaa3b68724"

    class FileDialog(object):
        def __init__(self, ext):
            self.ext = ext
            self.search_term = ""

            if isinstance(self.ext, basestring):
                self.ext = (self.ext,)

            basedir = config.basedir.replace('\\', os.sep)
            self.current_path_list = basedir.split(os.sep)

        @property
        def current_path(self):
            return str(os.sep).join(self.current_path_list)

        def go_upper_level(self):
            self.current_path_list.pop()
            return

        def enter_folder(self, folder):
            self.current_path_list.append(folder)
            return

        def get_folders(self):
            def filter_func(x):
                absolute_path = os.path.join(self.current_path, x)
                return os.path.isdir(absolute_path)

            rv = filter(filter_func, self.list_contents())

            del filter_func
            return rv

        def get_files(self):
            def filter_func(x):
                absolute_path = os.path.join(self.current_path, x)
                return os.path.isfile(absolute_path)

            rv = filter(filter_func, self.list_contents())
            del filter_func

            return filter(lambda x: x.endswith(tuple(self.ext)), rv)

        def change_folder_level(self, idx):
            self.current_path_list = self.current_path_list[:idx + 1]
            return

        def list_contents(self):
            rv = sorted(os.listdir(self.current_path))
            return [ i for i in rv if self.search_term.lower() in i.lower() ]

        def return_file(self, file):
            return os.path.join(self.current_path, file)

    class DDLCZipProcessor(object):
        whitelist = ["images.rpa", "audio.rpa", "fonts.rpa"]

        def __init__(self, ddlc_zip_path):
            self.ddlc_zip_path = ddlc_zip_path
            self.next_progress = 0
            self.archive = zipfile.ZipFile(self.ddlc_zip_path, "r")

        def __del__(self):
            self.archive.close()

        def filter_files(self, x):
            return any( (i in x.filename) for i in self.whitelist )

        def hash_check(self):
            if not os.path.exists(self.ddlc_zip_path):
                return None

            import hashlib
            buffer_size = 64 * 1024 # 64kb in bytes
            md5 = hashlib.md5()

            with open(self.ddlc_zip_path, 'rb') as f:
                while True:
                    chunk = f.read(buffer_size)
                    if not chunk:
                        break
                    md5.update(chunk)

            hash = md5.hexdigest()
            return hash

        def start_extract(self):
            file_info_list = filter(self.filter_files, self.archive.infolist())

            for i, file in enumerate(file_info_list):
                filename = os.path.split(file.filename)[-1]
                target_path = os.path.join(config.gamedir, filename)

                with self.archive.open(file) as rpa, open(target_path, "wb+") as target:
                    while True:
                        self.progress(target.tell(), file.file_size, filename)

                        chunk = rpa.read((10 ** 7))
                        if not chunk:
                            break

                        target.write(chunk)

        def done(self):
            ui.pausebehavior(0)
            renpy.call_screen(
                _screen_name="message",
                message="Restarting..."
            )

        def progress(self, progress, count, file_name):
            if (progress > 0) and (time.time() < self.next_progress):
                return

            ui.pausebehavior(0)
            renpy.call_screen(
                _screen_name="progress",
                progress=progress,
                count=count,
                file_name=file_name
            )

            self.next_progress = time.time() + .05

label choose_ddlc_zip:
    call screen dialog("DDLC archive files not found in /game folder\nPlease choose the DDLC zip.", Return())

    python hide:
        while True:
            ddlc_zip_path = renpy.call_screen(
                "file_dialog",
                (".zip",)
            )

            if not os.path.exists(ddlc_zip_path):
                file_exist_error = renpy.call_screen(
                    _screen_name="confirm",
                    message="Error loading in the selected file. Do you want to reselect the file or quit?", 
                    yes_action=Return(True), 
                    no_action=Return(False)
                )

                if file_exist_error:
                    continue
                else:
                    renpy.quit()

            processor = DDLCZipProcessor(ddlc_zip_path)

            if not processor.hash_check() in [ ddlc_mac_zip_hash, ddlc_win_zip_hash ]:
                rv = renpy.call_screen(
                    _screen_name="confirm",
                    message="MD5 Checksums do not match.\nDo you want to continue with this file?", 
                    yes_action=Return(True), 
                    no_action=Return(False)
                )

                if rv is False:
                    continue

            processor.start_extract()
            processor.done()

            break

        renpy.utter_restart()

screen file_dialog(ext):
    style_prefix "file_dialog"

    default file_dialog = FileDialog(ext)
    predict False

    add "#2e2e2e"

    frame:
        has vbox:
            spacing 20
        use file_dialog_path(file_dialog)
        use file_dialog_search(file_dialog)
        use file_dialog_selector(file_dialog)

style file_dialog_frame:
    background None
    padding (20, 20)

screen file_dialog_search(file_dialog):
    style_prefix "file_dialog_search"

    hbox:
        label _("Filter: ")
        frame:
            input value FieldInputValue(file_dialog, "search_term", True)

style file_dialog_search_hbox:
    spacing 15

style file_dialog_search_label is empty
style file_dialog_search_label_text is empty

style file_dialog_search_label:
    size_group "file_dialog"
    padding (5, 5)
    yalign 0.5

style file_dialog_search_label_text:
    size 20
    font gui.default_font

style file_dialog_search_frame:
    xfill True yalign 0.5
    background Transform(RoundedFrame(Solid("#DCC8A0")).add_radius(15.0), alpha=0.2)
    padding (15, 5)

style file_dialog_search_input:
    xalign 0.0 yalign 0.5
    yoffset 2

screen file_dialog_path(file_dialog):
    style_prefix "file_dialog_path"

    hbox:
        label _("Path: ")

        frame:
            viewport:
                mousewheel "horizontal"

                has hbox:
                    style "file_dialog_path_hbox"

                for i, folder in enumerate(file_dialog.current_path_list):
                    textbutton _("[folder]") action Function(file_dialog.change_folder_level, i)
                    if folder:
                        text _(" {folder_connect} ") yalign 0.5 color gui.insensitive_color

style file_dialog_path_label is empty
style file_dialog_path_button is empty
style file_dialog_path_frame is empty

style file_dialog_path_frame:
    yalign 0.5
    background Transform(RoundedFrame(Solid("#DCC8A0")).add_radius(15.0), alpha=0.2)
    padding (5, 5)

style file_dialog_path_viewport:
    xalign 0.5 yalign 0.5
    ysize 30

style file_dialog_path_hbox:
    xalign 0.5 yalign 0.5
    spacing 15

style file_dialog_path_label:
    size_group "file_dialog"
    yalign 0.5
    padding (5, 5)

style file_dialog_path_label_text:
    size 20
    font gui.default_font

style file_dialog_path_button:
    yalign 0.5

style file_dialog_path_button_text:
    xalign 0.5
    font gui.interface_font

screen file_dialog_selector(file_dialog):
    style_prefix "file_dialog_selector"
    predict False

    viewport id "file_dialog":
        scrollbars "vertical"
        mousewheel True
        has vbox:
            use file_dialog_entry(_("Upper Level"), "{upper_level}", Function(file_dialog.go_upper_level))

            null height 10

            for folder in file_dialog.get_folders():
                use file_dialog_entry(folder, "{folder}", Function(file_dialog.enter_folder, folder))

            null height 10

            for file in file_dialog.get_files():
                use file_dialog_entry(file, "{file}", Function(file_dialog.return_file, file))

screen file_dialog_entry(button_label, button_icon, button_action):
    style_prefix "file_dialog_entry"
    textbutton _("[button_label]"):
        action button_action
        foreground HBox(
            Text(
                button_icon, 
                style="file_dialog_entry_icon_text"
            ), 
            style="file_dialog_entry_icon_hbox"
        )

style file_dialog_entry_button is empty

style file_dialog_entry_icon_hbox is empty
style file_dialog_entry_icon_text is file_dialog_entry_button_text

style file_dialog_entry_button:
    padding (0, 5)
    xfill True
    left_padding 45
    xalign 0.0

style file_dialog_entry_button_text:
    size 20
    xalign 0.0

style file_dialog_entry_icon_hbox:
    yfill True

style file_dialog_entry_icon_text:
    size 20
    color gui.accent_color
    yalign 0.5
    xalign 0.05

screen message(message):
    tag interface

    style_prefix "message"
    add "#2e2e2e"

    label _("[message]")

style message_vbox is empty
style message_label is empty
style message_label_text is empty

style message_label:
    xalign 0.5 yalign 0.5

style message_label_text:
    font "mod_assets/gui/font/AlegreyaSansSC/AlegreyaSansSC-Regular.ttf"
    size 36

screen progress(progress, count, file_name):
    tag interface
    style_prefix "progress"
    add "#2e2e2e"

    vbox:
        bar style_suffix "file_bar":
            value progress range count

        label _("[file_name]")

style progress_vbox is empty
style progress_bar is empty
style progress_file_bar is empty
style progress_label is empty

style progress_vbox:
    spacing 10
    xalign 0.5 yalign 0.5

style progress_bar:
    left_bar gui.accent_color
    right_bar Null()
    ymaximum 24
    xsize 500

style progress_file_bar:
    left_bar gui.accent_color
    right_bar Null()
    ymaximum 24
    xsize 900

style progress_label:
    xalign 0.5

style progress_label_text:
    font "mod_assets/gui/font/AlegreyaSansSC/AlegreyaSansSC-Regular.ttf"
