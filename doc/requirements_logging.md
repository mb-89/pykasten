common things we want from logging:

1) [x] logging to console
2) [x] logging to files, either one file, or files with max size, or ringbuffer
3) [x] format: usually either time / source / lvl / msg or ms_since_start instead of time
4) [x] since programs are modular, sources should be able to be added dynamically.
5) [x] loglevel is handled globally.
6) [x] log into gui widgets, where we can filter
7) [x] last log-msg in gui status bar, so we dont have to have the logwidget open.
8) [ ] log to teams, with dedicated loglevel (betw. warn and err)
9) [x] is compatible with a lot of other tech, like interactive consoles, guis, etc.