-- args: number
SELECT completerID, COUNT(*) total
FROM posts
GROUP BY completerID
ORDER BY total DESC
LIMIT {};
