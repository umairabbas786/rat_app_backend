def write_from_iterable(writeable_file, iterable, suffix='', prefix=''):
    for i in iterable:
        writeable_file.write(f'{prefix}{i}{suffix}')
