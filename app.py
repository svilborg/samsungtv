import getopt
import sys

from samsungtv import SamsungTvApp


def usage_option(name, description):
    return "\t--%s     \t %s" % (name, description)


def usage():
    print ""
    print "Usage: " + sys.argv[0] + " [OPTIONS]"
    print usage_option("scan", "SSPD Scan")
    print usage_option("volume", "Set Volume")
    print usage_option("volup", "Incr Volume")
    print usage_option("voldown", "Decr Volume")
    print usage_option("help", "This help menu")
    print usage_option("start_httpd", "Start http server")
    print usage_option("stop_httpd", "Stop http server")
    print ""


if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:], "s:hv", ["help", "version",
                                                          "scan", "rescan",
                                                          "volume=", "volup", "voldown", "mute", "unmute",
                                                          "file=", "add_file=",
                                                          "play", "stop", "next", "prev",
                                                          "start_httpd", "stop_httpd",
                                                          "app=", "app_on=", "app_off=", "app_install=",
                                                          "key=", "keys", "apps", "launch="
                                                          ])
    except getopt.GetoptError, err:
        print(err)
        sys.exit(-1)

    for o, arg in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-V", "--version"):
            print VERSION
            sys.exit(0)
        elif o in ("-s", "--scan"):
            SamsungTvApp.scan()
        elif o in ("--rescan"):
            SamsungTvApp.scan(True)
        else:
            tv = SamsungTvApp()

            method = o.replace("--", "")
            print tv.run(method, arg)
