DROP table if exists recommendation;
CREATE TABLE `recommendation` (
  `recommend` TEXT not null,
  `commit_sha`  TEXT not null,
  `username` 	TEXT not null,
  `timestamp` TEXT not null,
  `commit_message`  TEXT,
  `repo_url`  TEXT,
  PRIMARY KEY(commit_sha)
);
