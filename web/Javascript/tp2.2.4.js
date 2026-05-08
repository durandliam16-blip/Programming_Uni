'use strict';

function Album(data) {
    Object.assign(this, data);
}

Album.prototype.getTitle = function() { return this.title; };
Album.prototype.getArtist = function() { return this.artist; };
Album.prototype.getYear = function() { return this.year; };

const myAlbum = new Album({ title: 'TitreTest', artist: 'ArtistTest', year: 2000 });
console.log(myAlbum.getArtist());