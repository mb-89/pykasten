common things we want from logging:

1) [ ] logging to console
2) [ ] logging to files, either one file, or files with max size, or ringbuffer
3) [ ] format: usually either time / source / lvl / msg or ms_since_start instead of time
4) [ ] since programs are modular, sources should be able to be added dynamically.
5) [ ] loglevel is handled globally.
6) [ ] log into gui widgets, where we can filter
7) [ ] last log-msg in gui status bar, so we dont have to have the logwidget open.
8) [ ] log to teams, with dedicated loglevel (betw. warn and err)
9) [ ] is compatible with a lot of other tech, like interactive consoles, guis, etc.