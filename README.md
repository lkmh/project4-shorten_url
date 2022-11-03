# GA Project 4 - Short It

## Objective:

Create shorter aliases for long URL

Original url:

<aside>
💡 https://stackoverflow.com/questions/43002444/make-axios-send-cookies-in-its-requests-automatically

</aside>

Output: users of the website can share this shorter link with friends

<aside>
💡 https://domain.com/57fdf6c

</aside>

## Functional Requirements

- Given a long url, generate a unique shorter URL for each user. i.e. even when another user gives the same url, a different shorter URL would be generated. Shorter URL should be random and unable to link back to the original URL
- Providing a shorter url, users would be redirected to the original link with minimal latency
- Providing a shorter url, users would be redirected to the original link with minimal latency
- Given a long url, generate a QR code as well as a shorter unique URL
- Users can sign and login to see analytics - view count of shorter URL generated. Users can reset password independently

## Planning

1. There is likely to be more re-directs compared to new URL shorten. ⇒ Assume 100:1 ratio between read and write 
2. Traffic estimates: 10M re-directs per month, assuming a 100:1 read/write ratio, we can expect 100k new URL during the period 
    1. New URL shorten per minute ⇒ 100k / (30 days * 24 hours * 60 min) ⇒ 2.3 per min
    2. URLs redirect per minute ⇒ 10M ((30 days * 24 hours * 60 min) ⇒ 231 per min
3. Storage estimates: Storing every URL for 5 years 
    1. 100k new URL per month X 5 years X12 months ⇒ 6M 
    2. 1 URL shouldnt be bigger than 255 bytes (FYI based **[on a data set of 6.6m unique URL, 78k unique domains](http://www.supermind.org/blog/740/average-length-of-a-url-part-2)** ⇒ average 77bytes )
    3. Storage required:  255 * 6B ⇒ 1.5B bytes of 1.5GB 
        1. elephantsql free 20mb is not enough 
4. Memory Estimates: 10M/30 * 20% * 500btyes ⇒ 33 MB

## Tech Stack

1. Frontend ⇒ HTML, CSS, JS
    1. I have used React already. Given that re-direct are 100:1, the frontend will be less used by user base
2. Backend ⇒ Fastapi 
    1. It is FAST and auto generates the schema. 
    2. JWT in cookies - with refresh and access token with logout 
    
    [https://project4-short-url.herokuapp.com/docs](https://project4-short-url.herokuapp.com/docs)
    
3. Storage ⇒ Postgres SQL 
    1. Structured data, also i tried mongo in project 2 
    
    Table: Users
    
    ![Untitled](GA%20Project%204%20-%20Short%20It/Untitled.png)
    
    Table Urls
    
    ![Untitled](GA%20Project%204%20-%20Short%20It/Untitled%201.png)
    
4. Table : URL_views
    
    ![Untitled](GA%20Project%204%20-%20Short%20It/Untitled%202.png)
    

Cache ⇒ Redis

1. Fast 
2. Key - [hash_url] = Value [Original_URL] 
3. So when Re-Direct route, 
    
    a) check if key is in redis, if True, get value 
    
    b) if key not in redis, go to SQL get value then cache in redis 
    

**The more important implementation:**

1. Hashing ⇒ 4 character hash is more than enough for 6M URLs
    
    We can use base64 ([A-Z, a-z, 0-9]) + / 
    
    6M URLs ⇒ 64**4 characters ⇒ 16.7m unique strings can be generates
    
    Coded for 5 characters ⇒ potentially 1billion at base 64
    
    Coded for 5 characters ⇒ potentially 600M at base 36
    
    Check for uniqueness of hash if not unique use hash (original_url + bcrypt.gensalt()) [gensalt inserts random string] 
    
2. Redis cache
    
    Free versions of Heroku and ElephantSQL makes it super slow to retrieve data from the SQL then redirect the use
    
    Cache commonly used hash in redis so that we don’t need to go to the SQL database for data
    
    Note: commonly used hash, means currently retrieved hash that is not in redis 
    

**More random implementation:**

1. Password reset (independently)
    
    Users can password reset if they forget the password by inputting their email
    
    System will generate a hash by take a specific portion of their hash old password and email to the user
    
    User than can input the hash, email and new password
