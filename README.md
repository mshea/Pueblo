Title: Pueblo: Python Markdown Blog Software
Author: Mike Shea
Date: 15 December 2011

## 30 second summary

I decided to formalize the script I use to generate this website and my other big website, Sly Flourish and [release it](http://mikeshea.net/pueblo.zip). Pueblo is a single python script that generates a blog of static HTML files from a directory full of [markdown](http://daringfireball.net/projects/markdown/) text files. It's small, fast, easy, secure, and extensible. While it doesn't have many of the features of bigger blog platforms, Pueblo lets you spend less time on website maintenance and more time writing.

## A single simple script

Pueblo is a single Python script that, when run, generates HTML files, an index file, an archive file, and an RSS feed from a set of markdown formatted text documents. If you're looking for a more full-featured blogging platform, one where you don't have to mess with the code itself, this *isn't* for you. Pueblo is primarily built to run my own websites, MikeShea.net and SlyFlourish.com. I wanted to release the code out there in case others could benefit from it or might teach me how to make it better.

## HTML generation from Markdown files

At its core, Pueblo uses Markdown files to generate HTML. These Markdown files include a subset of MultiMarkdown metadata to generate page titles, dates, and author links. These markdown files must have a .txt extension, must be in either ASCII or UTF8, and must have the title, author, and date fields in order. You can look at the [markdown for this article](pueblo.txt) as an example.

The configuration lets you exclude certain .txt files in case you don't want them.

The generated index.html file uses a stylesheet called "style.css" that uses [responsive web design](http://www.alistapart.com/articles/responsive-web-design/) to fit well onto many screens. The script also calls a file called "sidebar.html" to display aside content.

## The advantages of static HTML generation

There are many advantages to a blog that generates static HTML. For one, you are putting CPU processing time where it belongs, crunching articles when you WRITE them not when your readers READ them. Most blogging platforms store your articles in a structured database. Every time a reader hits your site, it has to reach into that database and generate a page. There are lots of ways to speed up that process but much easier is to simply serve a static web page. This lets the website scale much better than any sort of server-side code execution.

Static HTML means your site will be very very fast.

## Archiving your website

The ability to easily archive and transport your site is another big advantage to static HTML generation. If you decide your days running the blog are over but you want to keep the site, you can just copy all the text and HTML files and the site can live anywhere you want to put it. All of the generated URLs in Pueblo are locally referenced so you can even copy it to a thumb drive and still run the site like you would normally.

This means, years from now, you can still see your website as it ran without having to run a huge out-of-date blogging platform to see it.

## Security

Static HTML is also inherently secure. Instead of constantly dealing with hackers attempting to find vulnerabilities in your server-executed code, you only serve static HTML. There's no code to hack. The script itself runs only when you run it either with a cronjob or as a single-run CGI script. There are no parameters accepted so you don't need to worry about dealing with bad data getting passed through. Securing the script and your website are still important but it's much easier than having to constantly and continually update your code (I'm looking at you Wordpress).

## Few features

The disadvantage to a script like this is the lack of features. There's [no comment board](http://www.mikeshea.net/No_Comments.html), no ping backs, no plugins, no built-in search, no workflow system, and no other advanced blogging features. Again, if these features are important to you, look elsewhere. This script does have two collaborative features. First, it generates a 20 article RSS file called index.xml and second, it lets your readers link articles on Twitter referenced back to your account. It also includes Google Analytics and Amazon referral requests, mainly because I use these on my own sites. Other than that, the features are very slim.

## Make it your own

I expect the users of this script to know some Python and thus I expect you to make this script your own. I don't plan on doing a lot of updates or adding a lot of features so you should feel free to edit it as you see fit. A lot of the HTML generation is embedded in the script so you'll need to dig a little deeper to modify the code. That said, I hope you will build this script into the perfect script to run your site.

If you like Pueblo and want to give back, please bookmark and [use this Amazon link](http://www.amazon.com/?&tag=mikesheanet-20) to throw a few bucks my way while you pick up that [copy of Deadwood](https://www.amazon.com/dp/B001FA1OTU/ref=as_li_ss_til?tag=mikesheanet-20&camp=0&creative=0&linkCode=as4&creativeASIN=B001FA1OTU&adid=1XFEFB00DMH2B1ZRDDMP&) you've always wanted to buy.