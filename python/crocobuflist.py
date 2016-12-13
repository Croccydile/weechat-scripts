SCRIPT_NAME = "crocobuflist"
SCRIPT_AUTHOR = "Chompy Crocodylus <kthxbye@gmail.com>"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC = "Croccydiles Buffer List"
SCRIPT_DEBUG_COMMAND = "cbl_test"
SCRIPT_CLOSE = "cbl_close"

try:
    import weechat
    import_ok = True
except:
    print("This script must be run under WeeChat.")
    print("Get WeeChat now at: http://www.weechat.org/")
    import_ok = False

cbl_buffer = None


def cbl_close(*kwargs):
    return weechat.WEECHAT_RC_OK


def cbl_build_callback(data, item, window):
    output_str = ""

    # read infolist "buffer", to get list of buffers
    infolist = weechat.infolist_get("buffer", "", "")
    if infolist:
        while weechat.infolist_next(infolist):
            name = weechat.infolist_string(infolist, "name")
            output_str += name
            output_str += "\n"
        weechat.infolist_free(infolist)

    weechat.prnt("", "Build callback...\n" + output_str)

    return output_str


def cbl_update_callback(data, signal, signal_data):
    weechat.bar_item_update(SCRIPT_NAME)
    return weechat.WEECHAT_RC_OK


def cbl_debug_command(data, buffer, args):
    weechat.prnt("", "Forcing callback update...")
    weechat.bar_item_update(SCRIPT_NAME)
    return weechat.WEECHAT_RC_OK

# ==================== Main routine ====================

if __name__ == "__main__" and import_ok:
    if weechat.register(
            SCRIPT_NAME,
            SCRIPT_AUTHOR,
            SCRIPT_VERSION,
            SCRIPT_LICENSE,
            SCRIPT_DESC,
            SCRIPT_CLOSE,
            ""):

        version = weechat.info_get("version_number", "") or 0

        if int(version) >= 0x00030600:

            weechat.prnt("", "Creating new bar item callback...")
            cbl_bar_item = weechat.bar_item_new(
                SCRIPT_NAME,
                "cbl_build_callback",
                "")

            weechat.prnt("", "Creating new bar defaults...")
            cbl_bar = weechat.bar_new(
                SCRIPT_NAME,
                "off",                  # hidden
                "0",                    # priority
                "root",                 # type
                "",                     # condition
                "top",                  # position
                "columns_horizontal",   # filling_top_bottom
                "vertical",             # filling_left_right
                "0",                    # size
                "0",                    # size_max
                "default",              # color_fg
                "default",              # color_delim
                "default",              # color_bg
                "on",                   # separator
                SCRIPT_NAME)

            weechat.prnt("", "Setting bar options...")
            weechat.bar_set(
                cbl_bar,
                "filling_top_bottom",
                "columns_horizontal")
            weechat.bar_set(
                cbl_bar,
                "filling_left_right",
                "vertical")
            weechat.bar_set(
                cbl_bar,
                "separator",
                "on")

            weechat.prnt("", "Creating hook callbacks...")
            weechat.hook_signal(
                "buffer_line_added",
                "cbl_update_callback",
                "")
            weechat.hook_signal(
                "window_scrolled",
                "cbl_update_callback",
                "")
            weechat.hook_signal(
                "buffer_switch",
                "cbl_update_callback",
                "")

            weechat.hook_command(
                SCRIPT_DEBUG_COMMAND,
                SCRIPT_DESC,
                "Debug command to test buffer name generation\n",
                "",
                "",
                "cbl_debug_command",
                "")

            weechat.bar_item_update(SCRIPT_NAME)
        else:
            weechat.prnt(
                "",
                "%s%s %s" %
                (weechat.prefix("error"),
                 SCRIPT_NAME,
                 ": needs version 0.3.6 or higher"))
