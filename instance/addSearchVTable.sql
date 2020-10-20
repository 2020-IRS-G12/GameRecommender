CREATE VIRTUAL TABLE searchGameTable USING fts4(
  gameId INTEGER,
  description CHAR,
  title CHAR(73),
  genre CHAR(65) ,tokenize=porter);
INSERT INTO searchGameTable(gameId, description, title, genre) SELECT gameId, description, title, genre FROM GameDetail;
