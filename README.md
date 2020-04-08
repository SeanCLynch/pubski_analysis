# Process and Code Snippets for Pubski Research

## Basic Data Gathering

Navigate to Hubski and search for #pubski. Scroll to the bottom and click "more" until there are no more posts to load. I then saved this page, so that I could politely query it without hitting the live servers. Now we have a `pubski_list.html` file!

Next, I loaded that page in my browser (right click, open with...), and iteratively experimented until I produced the following code snippet, which is run in the browser console. It outputs a JSON array of the posts with their relevant info, which you can right-click on (in the browser console) and save as `pubski_list.json`.

```
let pubs_divs = document.querySelectorAll('#unit');
let pubs_array = [];
pubs_divs.forEach(function (pub, idx) { 
        let hubwheel	    = pub.querySelector('.plusminus .score a').className;
        let hubwheel_dots   = hubwheel.slice(-1);

        let title	= pub.querySelector('.feedtitle span a span').innerText;
        let post_date	= title.slice(7);
        let post_link	= pub.querySelector('.feedtitle span a').getAttribute('href');

        let comment_count = pub.querySelector('.feedcombub > a').innerText;
        let top_commenter = pub.querySelector('.feedcombub a').innerText;
        
        let badges = pub.querySelector('.titlelinks a.ajax');
        let multiple_badges = pub.querySelector('.titlelinks a.ajax b');
        let num_badges = (multiple_badges ? multiple_badges.innerText.slice(-1) : 
                                    badges ? 1 :
                                    0);

	pubs_array.push([
            title,
            post_date,
            post_link,
            comment_count,
            top_commenter,
            hubwheel_dots,
            num_badges
        ]);
});
console.log(pubs_array);
```

Next, I wanted to convert the JSON into a CSV, so that I could use spreadsheet software to make pretty graphs easily. I hadn't used 'jq' before but had heard good things, so in the terminal I typed: `sudo apt-get install jq`. Then, after some searching around, I found some docs & some code snippets that led me to create the following code, which outputs a `pubski_list.csv` file. 

`cat pubski_list.json | jq -r '(.[0] | keys_unsorted) as $keys | $keys, map([.[ $keys[] ]])[] | @csv' > pubski_list.csv`


## Basic Data Processing

Using the data (pubski_list.json, pubski_list.csv), I could easily measure technical and social attributes of Pubski, like number of pubski posts (total 268), comment count (average 77), badge count (average 1, median 0), most common top_commentor (kleinbl00, 28 times, 11% of Pubski posts), first post id (172369), current post id (427729). I can even create more advanced charts like:

number of comments over time [[GRAPH]]
or 
most frequent top commentor [[GRAPH]]

I also manually combed through the data, checking for any anomlies and found two things. First, that there are exactly three posts that used the '#pubski' and were not related to the weekly post whatsoever. It's very likely that these users were posting about a topic, and the Hubski recommendation system suggested '#pubski'. These posts were deleted prior to data processing. Here are those posts:

Realbeer.com: Beer News: The most beers on tap?, http://www.realbeer.com/news/articles/news-000246.php, 0 comments
Pico countertop craft automatic brewery for the inexperienced home brewer, http://www.gizmag.com/pico-countertop-automated-craft-beer-brewing-machine/40063/, 0 comments
Introducing Glyph, https://endlesswest.com/glyph/, 2 comments

The other anomly was two 'meta' posts about Pubski. Both related to the timing of Pubski and the belief that something was disrupting the normal scheduling of Pubski. These were kept in the dataset prior to processing. You can see them below:

'Pubski: July 25, 2018 [closed]', http://hubski.com/pub/412363, 10 comments
'Is it just me or was there no pubski last week?', http://hubski.com/pub/424500, 4 comments

All of this data is nice, but doesn't tell us too much about any individual Pubski, so let's dig deeper!

## Advanced Data Gathering

Now, with the list of (hundreds of) pubski posts in JSON & CSV, I could start to think about how we might crawl the list of Pubski links and get static versions of each individual page. One option is to use curl (or wget) in a bash script to fetch all the pages, then use something like cheerioJS to parse the resulting html files. Alternatively, we could use something like phantomJS (rip), slimerJS, casperJS, jsdom, etc to fully render the page and then perform some queries. Either way, the script will probably be bash or nodejs, languages I'm most framiliar with :)

One question though before I start scripting is what data do I need from each page? What I really want to create is a network-based representation of each Pubksi and perfrom an automated method of checking said network for different properties. After some thought, the automatic analysis step may have to be done in a different language (maybe python?), node and javascript just don't have the proper tools. Then with those results, look for trends or statistically significant phenomena and use them as justification for sociological or anthropological concepts. 

Ideally a list of all users, posts, post scores, shared links, threads of discussion, etc. 
NODE = user
EDGE = shared pubski
SIZE = # posts (?)
centrality, etc. 

-------------------------------------- UP TO HERE HAS BEEN ADDED TO BLOG POST


## Advanced Data Processing


