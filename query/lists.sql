-- args: status
SELECT t.taskID, t.requesterID, r.link
FROM tasks t
LEFT JOIN trackers r ON t.taskID = r.taskID
WHERE t.status = "{}";
