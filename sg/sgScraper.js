import fs from 'fs'
import { sgQuery } from './sgQueries.js';


function processData(data) {
    const link = 'https://reverb.com/item/'
    const myData = data
    for (const listing of myData.data.listingsSearch.listings) {
        const make = listing.make
        const id = listing.id
        const model = listing.model
        // write to csv
        if (id) {
            fs.appendFile('sg_listings.csv', `${id},${listing.slug},${make},${model},${link + id + '-' + listing.slug}\n`, function (err) {
                if (err) throw err;
                // console.log('Saved!');
            });
        }
    }
}

let offset = 0
function fetchData() {
    const endpoint = 'https://rql.reverb.com/graphql'
    console.log(offset)
    fetch(endpoint, {
        method: 'POST',
        body: JSON.stringify(sgQuery(offset)),
        headers: {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
    }).then(res => res.json())
        .then(processData)
        .then(() => fetchData(offset += 45))
}

fetchData()