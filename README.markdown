feed2pod.site
===

This is a website that uses [feed2pod](https://github.com/kemayo/feed2pod) to create viable podcast feeds and then host them.

It's entirely a personal-use project. I use ifttt's rss+webhooks to ping when a feed needs to be updated.

Setup
---

You need Python 3 and cherrypy.

    $ git submodule init

Create a file called `TOKEN`, and put something in it which only you know.

Usage
---

Make a request to: `http://SITE/refresh?feed=FEEDURL&token=TOKEN`
