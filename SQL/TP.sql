-- Movie(mID, title, year_, director)
-- Reviewer(rID, name_)
-- Rating(rID, mID, stars, ratingDate)

--1 
SELECT title from Movie
    WHERE director = 'Steven Spielberg';
--2
SELECT title from Movie
    WHERE (year_  BETWEEN 1980 AND 2000) 
        AND ((director = 'Steven Spielberg') 
            OR (director = 'James Cameron'));
--3
SELECT title, director FROM Movie 
    INNER JOIN Rating ON Movie.mID = Rating.mID
    WHERE Rating.RATINGDATE = '22-JAN-2011';
--4
SELECT Reviewer.name_, Rating.stars, Rating.RATINGDATE FROM Reviewer
    INNER JOIN Rating ON Reviewer.rID = Rating.rID
    INNER JOIN Movie ON Rating.mID = Movie.mID
    WHERE Movie.title = 'Gone with the Wind';
--5
SELECT DISTINCT re1.name_, re2.name_
    FROM Reviewer re1, Reviewer re2, Rating ra1, Rating ra2
    WHERE ra1.mID = ra2.mID
        AND re2.rID = ra2.rID
        AND ra1.rID = re2.rID
        AND re1.name_ < re2.name_;