#!/usr/bin/env python
import sys
import subprocess
import datetime
import time
import sched
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
    parser.add_argument("--dry-run", action='store_true', default=False)

    args = parser.parse_args()

    if args.version:

        print("sleepguard version %s" % VERSION)
        sys.exit(0)

    elif args.time:

        h, m = _parse_time_arg(args.time)
        event_times = _make_events(h, m, args.warnings_freq, args.nb_warnings)
        _print_events(event_times)

        scheduler = sched.scheduler(time.time, time.sleep)

        _schedule_events(scheduler, event_times, args.dry_run)

        scheduler.run()

    else:

        print("Invalid arguments.")
        sys.exit(1)


def _parse_time_arg(time_arg):

    try:

        time_str_items = time_arg.split(":")
        if len(time_str_items) != 2:
            raise ValueError

        h_str, m_str = time_str_items

        h, m = int(h_str), int(m_str)

        if h < 0 or h >= 24 or m < 0 or m >= 60:
            raise ValueError

        return h, m

    except ValueError:
        print("Invalid time argument %s" % time_arg)
        sys.exit(1)


def _make_events(h, m, warnings_freq, nb_warnings):

    time_now = datetime.datetime.now()
    time_cutoff = time_now.replace(hour=h, minute=m, second=0, microsecond=0)

    total_delta = time_cutoff - time_now

    # In case current time and cutoff time are not in the same day
    if total_delta.days < 0:
        time_cutoff += datetime.timedelta(days=1)
        total_delta = time_cutoff - time_now

    warning_delta = datetime.timedelta(minutes=warnings_freq)
    event_times = reversed([time_cutoff - i * warning_delta for i in range(nb_warnings+1)])

    # Removing events that won't have time to happen
    event_times = [ev_time for ev_time in event_times if (ev_time - datetime.datetime.now()).total_seconds() > 0]

    return event_times


def _print_events(event_times):

    print("Planned events :")
    for i, ev_time in enumerate(event_times):
        if i < len(event_times) - 1:
            type_str = "WARNING"
        else:
            type_str = "SHUTDOWN"
        print("%s at %s" % (type_str, ev_time.strftime("%H:%M")))
    print("\n")


def _send_message(message):

    print(message)
    subprocess.run(["aplay", "bleep.wav"], stderr=subprocess.STDOUT)
    subprocess.run(["./notify-send-all", message], stderr=subprocess.STDOUT)


def _schedule_events(scheduler, event_times, is_dry_run):

    time_cutoff = event_times[-1]

    for i in range(len(event_times)):

        is_warning = (i < len(event_times) - 1)

        delta_to_event = (event_times[i] - datetime.datetime.now()).total_seconds()

        if is_warning:
            scheduler.enter(delta_to_event, 0, _do_warning, argument=(i, len(event_times), time_cutoff))
        else:
            scheduler.enter(delta_to_event, 0, _do_shutdown, argument=(is_dry_run,))


def _do_warning(index, nb_events, time_cutoff):

    message = "Sleepguard warning %d of %d (SHUTDOWN AT %s)" % (index+1, nb_events-1, time_cutoff.strftime("%H:%M"))
    if index == nb_events - 2:
        message += "\nLAST WARNING !"

    print(message)
    notification(message)

    return message


def _do_shutdown(is_dry_run):

    message = "SHUTDOWN"
    print(message)
    notification(message)

    if is_dry_run:
        print("Dry run : the poweroff command would be run here")
    else:
        subprocess.run(["poweroff"], stderr=subprocess.STDOUT)


if __name__ == '__main__':
    main()
