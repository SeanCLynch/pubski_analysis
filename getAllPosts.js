/* 
    ADVANCED DATA GATHERING PHASE

    FUN FACT: in the same directory as pubski_list.json, you can 
    run `http-server -p 8888 --cors` to serve the json files locally. 

    Once that is up and running, you can run `node getAllPosts.js` to 
    run this code and iterate though each pub every 30 seconds. This will take
    about 30s * 260 = ~130 min or 2+ hours (!). 

    The resulting data is saved as JSON and as GraphML such that we can create 
    JS-based visualiztions and we can use Python graph network analysis tools to 
    parse the GraphML. 
*/

let request = require('request');
let cheerio = require('cheerio');
let fs = require('fs');

let REQ_TIMER = 10000;
let HUB_NUM = 0;
let basic_data = require('./pubski_list.json');


let requestLoop = setInterval(function () {

    // End condition. 
    if (HUB_NUM >= basic_data.length) clearInterval(requestLoop);

    // Set current pubski to evaluate.
    let curr_pub = basic_data[HUB_NUM];

    request(curr_pub.post_link, function (error, response, body) {
        console.log(`\nhub #${HUB_NUM} - status: ${response && response.statusCode}`);

        // Feed the response into cheerio. 
        let $ = cheerio.load(body);

        // A. Get list of all users involved (nodes). 
        let nodes = [{
            "username": "Pubski",
            "num_posts": 1
        }];
        let all_comments = $('.outercomm');
        all_comments.each(function (idx, elem) {
            let username = $(this).find('#username a').text();
            let user_index = nodes.findIndex((elem) => {return elem.username == username;});
            if (user_index == -1) {
                nodes.push({ 
                    "username": username,
                    "num_posts": 1
                });
            } else {
                nodes[user_index].num_posts += 1;
            }
        });
        console.log(`hub #${HUB_NUM} - nodes: ${nodes.length}`);


        // B. Construct comment graph. 
        function addEdges ($, nodes, edges, group, prev_user_idx) {
            group.each(function () {
        
                // Skip main post. 
                if (($(this).attr('class') == 'sub') || ($(this).attr('class') == 'wholepub')) return;
        
                // For each top-comment, add edges. 
                if ($(this).attr('class') == 'outercomm') {
                    let username = $(this).find('#username a').text();
                    let curr_user_idx = nodes.findIndex((n) => { return n.username == username; });

                    let is_dup_edge = edges.some(function (e) { return ((e.source == curr_user_idx) && (e.target == prev_user_idx)); });

                    if (!is_dup_edge) {
                        edges.push({
                            "source": nodes[curr_user_idx].username,
                            "target": nodes[prev_user_idx].username
                        });
                        // edges.push({
                        //     "source": curr_user_idx,
                        //     "target": prev_user_idx
                        // });
                    }
                }
        
                // For each set of subcomments, repeat.
                if ($(this).attr('class') == 'subcom') {
                    let next_group = $(this).children().last().children();
                    let next_username = $(this).prev().find('#username a').text();
                    let next_user_idx = nodes.findIndex((n) => { return n.username == next_username; });
                    addEdges($, nodes, edges, next_group, next_user_idx);
                }
        
            });
        }
        let edges = [];
        let start_group = $('.whole').children().last().children();
        let start_user_idx = 0;
        addEdges($, nodes, edges, start_group, start_user_idx);
        console.log(`hub #${HUB_NUM} - edges: ${edges.length}`);


        // C-1. Save edgelist
        let edgelist_data = "";
        edges.forEach(function (edge) {
            edgelist_data += `${edge.source} ${edge.target}\n`;
        });
        fs.writeFileSync(`./pubski_data/${HUB_NUM}.edgelist`, edgelist_data);

        // C-2. Save JSON
        let json_data = JSON.stringify({
            "nodes": nodes,
            "edges": edges,
            "meta": curr_pub
        });
        fs.writeFileSync(`./pubski_data/${HUB_NUM}.json`, json_data);

        // Increment counter. 
        HUB_NUM++;
    });
}, REQ_TIMER);

