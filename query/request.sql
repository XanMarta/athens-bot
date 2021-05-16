-- args: requestLink, content, requesterID
INSERT INTO tasks (requestLink, requestedDate, content, status, requesterID)
VALUES ("{}", NOW(), "{}", "requesting", "{}");