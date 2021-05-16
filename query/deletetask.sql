-- args: taskID, taskID, taskID
DELETE
FROM trackers
WHERE taskID = {};

DELETE
FROM posts
WHERE taskID = {};

DELETE
FROM tasks
WHERE taskID = {};
