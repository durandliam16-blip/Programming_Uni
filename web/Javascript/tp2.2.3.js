'use strict';

const albums = require('./albums.json');

const albumTitle = (album) => album.title;
const albumArtist = (album) => album.artist;
const albumYear = (album) => album.year;

console.log(albumYear(albums['Ummagumma'])); // Affiche 1969