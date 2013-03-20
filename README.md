# Pueblo: Python Markdown Blog Software

## Updated 19 March 2013

I have significantly updated Pueblo since the last version. The main differences include using the [Jinja2](http://jinja.pocoo.org/docs/) module for HTML and RSS generation and switching it over to a library instead of a single script. The library is also written in an object-oriented style which makes it much easier to understand.

## 30 second summary

I decided to formalize the script I use to generate [mikeshea.net](http://mikeshea.net) and my other big website, [Sly Flourish](http://slyflourish.com) and [release it](https://github.com/mshea/Pueblo). Pueblo is a python script that generates a blog of static HTML files from a directory full of [markdown](http://daringfireball.net/projects/markdown/) text files. It's small, fast, easy, secure, and extensible. While it doesn't have many of the features of bigger blog platforms, Pueblo lets you spend less time on website maintenance and more time writing.

## A simple script

Pueblo is a Python library, launcher, and set of templates that, when run, generates HTML files, an index file, an archive file, and an RSS feed from a set of markdown formatted text documents. If you're looking for a more full-featured blogging platform, one where you don't have to mess with the code itself, this *isn't* for you. Pueblo is primarily built to run my own websites, [mikeshea.net](http://mikeshea.net) and [Sly Flourish](http://slyflourish.com). I wanted to release the code out there in case others could benefit from it or might teach me how to make it better.

## HTML generation from Markdown files

At its core, Pueblo uses [Markdown](http://daringfireball.net/projects/markdown/) files to generate HTML. These Markdown files include a subset of MultiMarkdown metadata to generate page titles, dates, and author links. These markdown files must have a .txt extension, must be in either ASCII or UTF8, and must have the title, author, and date fields in the proper order.

The configuration lets you exclude certain .txt files in case you don't want them.

The generated index.html file uses a stylesheet called "style.css" that uses [responsive web design](http://www.alistapart.com/articles/responsive-web-design/) to fit well onto many screens.

## Dependencies

This program requires two python packages, one for [markdown](https://pypi.python.org/pypi/Markdown) and [Jinja2](http://jinja.pocoo.org/docs/) for the rendering of the HTML and RSS templates. You will need to install these modules for this script to work.

## Getting It To Work

To begin, install the [Markdown](https://pypi.python.org/pypi/Markdown) and [Jinja2](http://jinja.pocoo.org/docs/) Python modules either through their installation scripts or by copying their module directories as subdirectories the root directory from which you plan to launch Pueblo (this is what I did to run it on my Pairlite server).

Next, customize the "build_site.py" file to set up your own HTML and template directories. Also add any .txt files it should ignore.

Next, modify the templates found in the templates directory to suit your preferences.

Finally, you can either run the "build_site.py" script as a CGI script or set up a cron-job to run it periodically.

## The advantages of static HTML generation

There are many advantages to a blog that generates static HTML. For one, you are putting CPU processing time where it belongs, crunching articles when you WRITE them not when your readers READ them. Most blogging platforms store your articles in a structured database. Every time a reader hits your site, it has to reach into that database and generate a page. There are lots of ways to speed up that process but much easier is to simply serve a static web page. This lets the website scale much better than any sort of server-side code execution.

Static HTML means your site will be very very fast.

## The Thousand Year Blog

The ability to easily archive and transport your site is another big advantage to static HTML generation. If you decide your days running the blog are over but you want to keep the site, you can just copy all the text and HTML files and the site can live anywhere you want to put it. All of the generated URLs in Pueblo are locally referenced so you can even copy it to a thumb drive and still run the site like you would normally.

This means, years from now, you can still see your website as it ran without having to run a huge out-of-date blogging platform to see it.

## Security

Static HTML is also inherently secure. Instead of constantly dealing with hackers attempting to find vulnerabilities in your server-executed code, you only serve static HTML. There's no code to hack. The script itself runs only when you run it either with a cronjob or as a single-run CGI script. There are no parameters accepted so you don't need to worry about dealing with bad data getting passed through. Securing the script and your website are still important but it's much easier than having to constantly and continually update your code (I'm looking at you Wordpress).

## Few Features

The disadvantage to a script like this is the lack of features. There's [no comment board](http://www.mikeshea.net/No_Comments.html), no ping backs, no plugins, no built-in search, no workflow system, and no other advanced blogging features. Again, if these features are important to you, look elsewhere. This script does have two collaborative features. First, it generates a 20 article RSS file called index.xml and second, it lets your readers link articles on Twitter referenced back to your account. It also includes Google Analytics and Amazon referral requests, mainly because I use these on my own sites. Other than that, the features are very slim.

## Released under the MIT Software License

I have released this software under the [MIT Software License](http://en.wikipedia.org/wiki/MIT_License). Please reference the license, included in the pueblo source code for information on use, modification, and redistribution.

If you like Pueblo and want to give back, please bookmark and [use this Amazon link](http://www.amazon.com/?&tag=mikesheanet-20) to throw a few bucks my way.