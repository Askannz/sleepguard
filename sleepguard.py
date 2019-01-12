#!/usr/bin/env python
import sys
import subprocess
import datetime
import time
import argparse

VERSION = 1.0


def notification(message):
    subprocess.run(["aplay", "bleep.wav"], stderr=subprocess.STDOUT)
    subprocess.run(["./notify-send-all", message], stderr=subprocess.STDOUT)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='store_true', help='Print version and exit.')
    parser.add_argument("-t", "--time", action='store')
    parser.add_argument("-n", "--nb-warnings", action='store', type=int, default=2)
    parser.add_argument("-f", "--warnings-freq", action='store', type=int, default=15)

    args = parser.parse_args()

    if args.version:

        print("sleepguard version %s" % VERSION)
        sys.exit(0)

    elif args.time:

        try:

            time_str_items = args.time.split(":")
            if len(time_str_items) != 2:
                raise ValueError

            h_str, m_str = time_str_items

            h, m = int(h_str), int(m_str)

            if h < 0 or h >= 24 or m < 0 or m >= 60:
                raise ValueError

        except ValueError:
            print("Invalid time argument %s" % args.time)
            sys.exit(1)

        time_now = datetime.datetime.now()
        time_cutoff = time_now.replace(hour=h, minute=m, second=0, microsecond=0)

        total_delta = time_cutoff - time_now

        # In case current time and cutoff time are not in the same day
        if total_delta.days < 0:
            time_cutoff += datetime.timedelta(days=1)
            total_delta = time_cutoff - time_now

        warning_delta = datetime.timedelta(minutes=args.warnings_freq)
        event_times = reversed([time_cutoff - i * warning_delta for i in range(args.nb_warnings+1)])

        # Removing events that won't have time to happen
        event_times = [ev_time for ev_time in event_times if (ev_time - datetime.datetime.now()).total_seconds() > 0]

        print("Planned events :")
        for i, ev_time in enumerate(event_times):
            if i < len(event_times) - 1:
                type_str = "WARNING"
            else:
                type_str = "SHUTDOWN"
            print("%s at %s" % (type_str, ev_time.strftime("%H:%M")))
        print("\n")

        for i in range(len(event_times)):

            delta_to_next_event = event_times[i] - datetime.datetime.now()
            time.sleep(delta_to_next_event.total_seconds())

            if i < len(event_times) - 1:
                message = "Sleepguard warning %d of %d (SHUTDOWN AT %s)" % (i+1, args.nb_warnings, time_cutoff.strftime("%H:%M"))

                if i == len(event_times) - 2:
                    message += "\nLAST WARNING !"

                print(message)
                notification(message)

            else:
                message = "SHUTDOWN"
                print(message)
                notification(message)
                subprocess.run(["poweroff"], stderr=subprocess.STDOUT)

    else:

        print("Invalid arguments.")
        sys.exit(1)


if __name__ == '__main__':
    main()
