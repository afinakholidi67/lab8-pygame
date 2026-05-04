instead of easy construction if x > WIDTH: x = 0  im using giving to coordinate  "-size" so squere smoothly fully will be hidden by the edage of our screen 
ex 7 
its pretty difficult in my eyes. anywas i started to work on it 
fisctly i added lenght 
then to create_squers ive added history
after i will add center to update_squers 
the last but not least part is drawing squers itself what i did 
im a little lost for the last part. right now it looks to ugly anf far from truth
When a square extends beyond the screen's border, the pygame.draw.lines function attempts to connect its last two points, resulting in a long line appearing across the entire window. To solve this, you need to track the distance between the points.]
Ex8 The frame's pixel measurement speed is compared with the velocity vector magnitude and the actual distance traveled between frames. This is done using the position history implemented in Exercise 7. To ensure the accuracy of the changes, we ignore frames where the square crosses the screen, so the speed there will be expectedly high. If the actual speed deviates from the expected speed by more than 1%, we print it to the console.