-- args: taskID
SELECT r.link, t.requesterID, t.content, t.status, t.requestLink, p.completerID, p.completeLink
FROM tasks t
LEFT JOIN trackers r ON t.taskID = r.taskID
LEFT JOIN posts p ON t.taskID = p.taskID
WHERE t.taskID = {};
