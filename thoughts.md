# Quick


### Which protocol will be used to access the images ?
http Rest or Websocket 

### Will it have viewOnce && 24 hour timeline
yes

### How will i track seen info from client side?
- for now most i can think of is the when the client will get the another person image it will if the images is sent successfully(200 ok) then i will mark that image that this user has seen it so never show him again...

-- Followup question , do i keep track of all the users that have seen that individual image ? 
in my architecture yes, har ek image ke users honge then see if its thier 1st time or not

-- Followup question , how will i allow restrictions then like only his friend can see ?
user1(with his credentials) -> user2/image1 -> (check user1 is friend of user2 ?){
    yes -> (check user1 has seen image1){
        yes -> null
        no -> image1{image1 add user1}
    }
    no -> unaccess
}

AI intervention: 
    The Bug2: Network delivery does not equal human sight. If the client app prefetches/caches the image in the background while the user is looking at a different screen, your server marks it as "seen." If the user closes the app right then, that image is lost forever without them ever actually laying eyes on it.

The Fix Hint: The server shouldn't guess. The client needs to explicitly tell the server when the image enters the viewport.

ME: so i need to create a frontend which does this 

AI : The Bug2: What happens when user1 and user2 are friends, user1 views the image (it gets marked seen), and the next day user2 unfriends user1? If user1 tries to request that image endpoint again, your logic evaluates check friend? first, returns no -> unaccess, which accidentally leaks information or handles the state incorrectly. More importantly, checking friendship on every single image item request is highly inefficient.
The WRONG IDEA : If this is an "Instant" feature broadcast to multiple friends, an image might be viewed by dozens or hundreds of people. Appending to a list inside a single image document/row introduces heavy write locks and database bloat for an ephemeral (24-hour) feature.


SO i have to come up with new concept>