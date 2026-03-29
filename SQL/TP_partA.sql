-- Movie(mID, title, year_, director)
-- Reviewer(rID, name_)
-- Rating(rID, mID, stars, ratingDate)

-- Partie A  : Selects basiquent
-- SQL procédural cd normal
-- SQL déclaratif cad comme Romain :
    /* SELECT t.A,t.B FROM R t,S u WHERE t.A>u.B AND t.ID=u.ID; */

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

--6 
(SELECT DISTINCT director AS name_ FROM Movie WHERE year_ < 1980)
UNION
(SELECT DISTINCT re.name_
    FROM Reviewer re
    JOIN Rating ra ON re.rID = ra.rID
    JOIN Movie m  ON m.mID = ra.mID
    WHERE m.director = 'Steven Spielberg');

--7
SELECT title, year_, director FROM Movie 
    WHERE mID NOT IN 
        (SELECT mID FROM Rating 
        JOIN Reviewer ON Rating.rID = Reviewer.rID
        WHERE Reviewer.name_ = 'Chris Jackson');

--8 
SELECT DISTINCT re.name_ FROM Reviewer re
    JOIN Rating ra ON ra.rID = re.rID
    JOIN Movie m ON m.mID = ra.mID
    WHERE m.director = 'Steven Spielberg'
        AND ra.stars = (SELECT MAX(stars) FROM Rating ra2
                            JOIN Movie m2 ON m2.mID = ra2.mID
                            WHERE m2.director = 'Steven Spielberg');

--9 

-- Double not exists
SELECT r.name_ FROM Reviewer r
    WHERE NOT EXISTS (SELECT m.mID FROM Movie m
                        WHERE m.director = 'Steven Spielberg' AND NOT EXISTS (
                            SELECT 1 FROM Rating ra
                                WHERE ra.rID = r.rID AND ra.mID = m.mID));
                            /* "Existe-t-il au moins une ligne dans Rating où cet évaluateur a noté ce film ?"
                            Si non, la sous-requête ne renvoie rien → NOT EXISTS devient vrai → ça veut dire :
                                "Cet évaluateur n’a pas noté ce film-là."*/

-- Not exists et not in 
SELECT r.name_ FROM Reviewer r
    WHERE NOT EXISTS (SELECT m.mID FROM Movie m
                        WHERE m.director = 'Steven Spielberg' AND m.mID NOT IN (
                            SELECT ra.mID FROM Rating ra
                                WHERE ra.rID = r.rID));
-- ressemble double not exists
/* Prend tout les gens qui ne sont pas dans la liste des gens qui n'ont pas tout noté */

-- Group by et having
SELECT r.name_ FROM Reviewer r
    JOIN Rating ra ON ra.rID = r.rID JOIN Movie m ON m.mID = ra.mID
    WHERE m.director = 'Steven Spielberg'
    GROUP BY r.rID, r.name_
    HAVING COUNT(DISTINCT m.mID) = (SELECT COUNT(*) FROM Movie WHERE director = 'Steven Spielberg');
/* Verif en comptants les reviews */

-- Jointure et comptage
SELECT r.name_ FROM Reviewer r
    LEFT JOIN (SELECT ra.rID, COUNT(DISTINCT ra.mID) AS nb FROM Rating ra
                JOIN Movie m ON m.mID = ra.mID
                WHERE m.director = 'Steven Spielberg'
                GROUP BY ra.rID) 
            x ON x.rID = r.rID WHERE x.nb = (SELECT COUNT(*) FROM Movie
                                                WHERE director = 'Steven Spielberg');