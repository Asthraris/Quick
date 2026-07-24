

1. How to check for unviewed images from friends on Login
When a user logs in (or fetches their main feed), you want to answer: "Show me active images posted by my friends that I haven't viewed yet."

Here is the database logic to achieve this using a SQL JOIN:

The Logic Steps:
Get all user IDs who are accepted friends with curr_user.

Filter images where uploader_id is in that friends list.

Filter out expired images (expiries_at > NOW()).

Exclude images already in image_views for curr_user.id using NOT EXISTS or a LEFT JOIN.

2. How the View-Once Flow Works in API Code
When a user requests to open/view an image (GET /images/{image_id}):

Check if expired: Verify expiries_at > NOW().

Check if already viewed: Query image_views for (image_id, curr_user.id). If present, return 403 Forbidden ("You have already viewed this image").

Record view & return image: Insert a row into image_views and return the image details.

1. GET /feed/unviewed   ---> Returns list of [ { id, uploader_id, posted_at } ]  (NO URL yet)
2. POST /images/{id}/view ---> Returns { url }  AND  logs the view to image_audit table! 