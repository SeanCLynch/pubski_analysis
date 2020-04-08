# Process and Code Snippets for Pubski Research

You can see a lot more info on my blog at: https://seans.pub

## Getting pubski_list.html

Navigate to Hubski and search for #pubski. Scroll to the bottom and click "more" until there are no more posts to load. I then saved this page, so that I could politely query it without hitting the live servers. Now we have a `pubski_list.html` file!

## Getting pubski_list.json

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

## Getting pubski_list.csv

Next, I wanted to convert the JSON into a CSV, so that I could use spreadsheet software to make pretty graphs easily. I hadn't used 'jq' before but had heard good things, so in the terminal I typed: `sudo apt-get install jq`. Then, after some searching around, I found some docs & some code snippets that led me to create the following code, which outputs a `pubski_list.csv` file. 

`cat pubski_list.json | jq -r '(.[0] | keys_unsorted) as $keys | $keys, map([.[ $keys[] ]])[] | @csv' > pubski_list.csv`
