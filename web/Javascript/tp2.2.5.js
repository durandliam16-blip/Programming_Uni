'use strict';
const data = require('./albums.json');

const albums = Object.fromEntries(
    Object.entries(data).map(([key, value]) => [key, new Album(value)])
);

console.log(albums['Hot Rats'].getArtist()); // Frank Zappa