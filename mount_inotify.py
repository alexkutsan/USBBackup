import inotify.adapters


def _main():
    i = inotify.adapters.Inotify()

    i.add_watch(b'/etc/mtab')
    try:
        for event in i.event_gen():
            print(event)
            if event is not None:
                (header, type_names, watch_path, filename) = event
                print(event)
    finally:
        i.remove_watch(b'/etc/mtab')

if __name__ == '__main__':
    _main()
