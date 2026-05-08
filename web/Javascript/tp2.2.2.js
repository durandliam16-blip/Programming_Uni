'use strict';

// q1
const albums = {
    "titre1": {artist: "Cream", date: 1996, album: "Fresh Cream"},
    "titre2": {artist:"Frank Zappa", date: 1969, album: "Hot Rats"},
    "Space Oddity": {artist: "David Bowie", date:1969},
    "Merry Christmas": "Mariah Carey",
    "Songs from a Room": "Leonard Cohen",
    "Ummagumma": "Pink Floyd",
    "Camembert Électrique": "Gong",
    "The Piper at the Gates of Dawn": "Pink Floyd"
};

// q2
function albumTitle(albums, titre) {
    console.log(albums[titre]["artist"]); 
}
albumTitle(albums,"titre1")