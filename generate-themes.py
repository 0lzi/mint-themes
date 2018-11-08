#!/usr/bin/python3
import os

def change_value (key, value, file):
    if value is not None:
        command = "sed -i '/%(key)s=/c\%(key)s=%(value)s' %(file)s" % {'key':key, 'value':value, 'file':file}
    else:
        command = "sed -i '/%(key)s=/d' %(file)s" % {'key':key, 'file':file}
    os.system(command)

def colorize_directory (path, variation):
    for accent in HEX_ACCENTS:
        os.system("find %s -name '*.*' -type f -exec sed -i 's/%s/%s/gI' {}  \\;" % (path, accent, hex_colors[variation]))
    for accent in RGB_ACCENTS:
        os.system("find %s -name '*.*' -type f -exec sed -i 's/%s/%s/gI' {}  \\;" % (path, accent, rgb_colors[variation]))

# Mint-X
HEX_ACCENTS = ["#9ab87c", "#accd8a"]

hex_colors = {}
hex_colors["Aqua"] = "#6cabcd"
hex_colors["Blue"] = "#5b73c4"
hex_colors["Brown"] = "#aa876a"
hex_colors["Grey"] = "#9d9d9d"
hex_colors["Orange"] = "#db9d61"
hex_colors["Pink"] = "#c76199"
hex_colors["Purple"] = "#8c6ec9"
hex_colors["Red"] = "#c15b58"
hex_colors["Sand"] = "#c8ac69"
hex_colors["Teal"] = "#5aaa9a"

RGB_ACCENTS = ["172, 205, 138", "#accd8a"]

rgb_colors = {}
rgb_colors["Aqua"] = "108, 171, 205"
rgb_colors["Blue"] = "91, 115, 196"
rgb_colors["Brown"] = "170, 135, 106"
rgb_colors["Grey"] = "157,157,157"
rgb_colors["Orange"] = "219, 157, 97"
rgb_colors["Pink"] = "199, 97, 153"
rgb_colors["Purple"] = "140, 110, 201"
rgb_colors["Red"] = "193, 91, 88"
rgb_colors["Sand"] = "200, 172, 105"
rgb_colors["Teal"] = "90, 170, 154"

if os.path.exists("usr"):
    os.system("rm -rf usr/")

os.system("mkdir -p usr/share/themes")

os.system("cp -R src/Mint-X/theme/* usr/share/themes/")

for color in os.listdir("src/Mint-X/variations"):
    path = os.path.join("src/Mint-X/variations", color)
    if os.path.isdir(path):
        theme = "usr/share/themes/Mint-X-%s" % color
        theme_index = os.path.join(theme, "index.theme")
        os.system("cp -R usr/share/themes/Mint-X %s" % theme)
        os.system("cp -R src/Mint-X/variations/%s/* %s/" % (color, theme))

        # Theme name
        for key in ["Name", "GtkTheme", "IconTheme"]:
            change_value(key, "Mint-X-%s" % color, theme_index)

        # Accent color
        gtkrc = os.path.join(theme, "gtk-2.0", "gtkrc")
        settings_ini = os.path.join(theme, "gtk-3.0", "settings.ini")
        gtk_main_css = os.path.join(theme, "gtk-3.0", "gtk-main.css")
        for file in [gtkrc, settings_ini, gtk_main_css]:
            for accent in HEX_ACCENTS:
                os.system("sed -i s'/%(accent)s/%(color_accent)s/' %(file)s" % {'accent': accent, 'color_accent': hex_colors[color], 'file': file})

        # Cinnamon theme name
        file = os.path.join(theme, "cinnamon", "theme.json")
        if os.path.exists(file):
            os.system("sed -i s'/Mint-X/Mint-X-%(color)s/' %(file)s" % {'color': color, 'file': file})

        # Cinnamon colors
        file = os.path.join(theme, "cinnamon", "cinnamon.css")
        if os.path.exists(file):
            for accent in HEX_ACCENTS:
                os.system("sed -i s'/%(accent)s/%(color_accent)s/' %(file)s" % {'accent': accent, 'color_accent': hex_colors[color], 'file': file})
            for accent in RGB_ACCENTS:
                os.system("sed -i s'/%(accent)s/%(color_accent)s/' %(file)s" % {'accent': accent, 'color_accent': rgb_colors[color], 'file': file})

# Mint-Y
os.chdir("src/Mint-Y")
os.system("./build-themes.py")
os.chdir("../..")

# Mint-Y color variations
for color in hex_colors.keys():
    for variant in ["", "-Dark", "-Darker"]:
        original_name = "Mint-Y%s" % variant
        path = os.path.join("src/Mint-Y/variations/%s" % color)
        if os.path.isdir(path):
            # Copy theme
            theme = "usr/share/themes/%s-%s" % (original_name, color)
            theme_index = os.path.join(theme, "index.theme")
            os.system("cp -R usr/share/themes/%s %s" % (original_name, theme))

            # Theme name
            for key in ["Name", "GtkTheme"]:
                change_value(key, "%s-%s" % (original_name, color), theme_index)

            for key in ["IconTheme"]:
                change_value(key, "Mint-Y-%s" % color, theme_index)

            for key in ["MetacityTheme"]:
                metacity_variant = original_name.replace("Darker", "Dark")
                change_value(key, "%s-%s" % (original_name, color), theme_index)

            # Accent color
            gtkrc = os.path.join(theme, "gtk-2.0", "*rc")
            gtkrc_toolbar = os.path.join(theme, "gtk-2.0", "menubar-toolbar", "gtkrc")
            gtk_main_css = os.path.join(theme, "gtk-3.0", "gtk.css")
            cinnamon_css = os.path.join(theme, "cinnamon", "cinnamon.css")
            metacity2_xml = os.path.join(theme, "metacity-1", "metacity-theme-2.xml")
            metacity3_xml = os.path.join(theme, "metacity-1", "metacity-theme-3.xml")
            for file in [gtkrc, gtkrc_toolbar, gtk_main_css, cinnamon_css, metacity2_xml, metacity3_xml]:
                if os.path.exists(file):
                    for accent in HEX_ACCENTS:
                        os.system("sed -i s'/%(accent)s/%(color_accent)s/gI' %(file)s" % {'accent': accent, 'color_accent': hex_colors[color], 'file': file})
                    for accent in RGB_ACCENTS:
                        os.system("sed -i s'/%(accent)s/%(color_accent)s/gI' %(file)s" % {'accent': accent, 'color_accent': rgb_colors[color], 'file': file})


            directories = []
            directories.append(os.path.join(theme, "cinnamon/common-assets"))
            directories.append(os.path.join(theme, "cinnamon/light-assets"))
            for directory in directories:
                if os.path.exists(directory):
                    colorize_directory(directory, color)

            # Assets
            os.system("rm -rf %s/gtk-3.0/assets" % theme)
            os.system("rm -rf %s/gtk-2.0/assets" % theme)
            if variant == "-Dark":
                os.system("cp -R %s/gtk-2.0/assets-dark %s/gtk-2.0/assets" % (path, theme))
            else:
                os.system("cp -R %s/gtk-2.0/assets %s/gtk-2.0/assets" % (path, theme))
            os.system("cp -R %s/gtk-3.0/assets %s/gtk-3.0/assets" % (path, theme))


# Files
os.system("cp -R files/* ./")
