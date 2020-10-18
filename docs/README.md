The idea for this project is to have some items from an RSS feed with clickable links scroll on a ticker that gets updated ever few minutes.  Eventually I'd like to build this into a cli tool that lets a user start and top the ticker, customize the colors, add and remove rss feeds, etc.

Maybe add a weather function, where if it's turned on, it will give the weather after every ~10 rss items.

TODO:
* Add fast forward/rewind feature
    * rewind will require me to save deleted text, and then add it as we go backward
* Add requirements
* Edit movewindow to work on maximized windows
    * Alternatively, try to make the ticker completely separate from stuff on the screen.  Make it behave kind of like the windows menu bar.
* Edit colors/style