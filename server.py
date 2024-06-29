
import sys
import cgi
import os
import requests
import Physics
import math
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qsl


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );

        # check if the web-pages matches the list
        if parsed.path in [ '/index.html' ]:

            # retreive the HTML file
            fp = open( '.'+self.path );
            content = fp.read();

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();

        # check if the web-pages matches the list
        elif parsed.path.startswith("/table-") and parsed.path.endswith(".svg"):
            # retreive the HTML file & insert form data into the HTML file
            fp = open( '.'+self.path, 'rb' );
            content = fp.read();

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "image/svg+xml" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the browser
            self.wfile.write(content);
            fp.close();

        else:
            # generate 404 for GET requests that aren't the 3 files above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );
    
    def do_POST(self):
        parsed = urlparse(self.path)

        
        if parsed.path in [ '/newIndex']:
            form = cgi.FieldStorage(fp=self.rfile,
                                    headers=self.headers,
                                    environ={'REQUEST_METHOD': 'POST',
                                    'CONTENT_TYPE': 
                                        self.headers['Content-Type'],
                                            }
                                    )
            
            # Incomplete logic at implementing the player names
            #player1Name = form["player1Name"].value
            #player2Name = form["player2Name"].value
            #print("Player 1 Name:", player1Name)
            #print("Player 2 Name:", player2Name)

   

            
            
            xVel = form["xVelocityValue"].value
            yVel = form["yVelocityValue"].value
            print(xVel)
            print(yVel)


                            

            
            counter=0
            while os.path.exists("table-%d.svg" %counter):
                os.remove("table-%d.svg" %counter)
                counter+=1

            # Compute the acceleration
            velocityValue = Physics.Coordinate(float(form["xVelocityValue"].value), float(form["yVelocityValue"].value))
            accelerationValue = Physics.Coordinate(0.0,  0.0)
            speed = Physics.phylib.phylib_length(velocityValue);
            
            if speed > Physics.VEL_EPSILON:
                accelerationValue.x = -velocityValue.x / speed * Physics.DRAG
                accelerationValue.y = -velocityValue.y / speed * Physics.DRAG

            table = Physics.Table()

            position = Physics.Coordinate(float(form["xCue"].value), float(form["yCue"].value))
            positionRolling = Physics.Coordinate(float(form["xVelocityValue"].value), float(form["yVelocityValue"].value))
            stillBall = Physics.StillBall(1, position)
            rollingBall = Physics.RollingBall(0, positionRolling, velocityValue, accelerationValue)

            table += stillBall
            table += rollingBall    

            # Save the generated tables in the same directory as the files
            x =  0
            while  table:
                with open("table-%d.svg" %(x), "w") as file:
                    file.write(table.svg())
                x+=1
                table = table.segment()

            # Nice HTML Page
            html_content = """
            <html>
                <head>
                    <title>My Pool Page</title>
                </head>
                <body>
                <a href= "/shoot.html">Back</a>
            """
            html_content+= "<p> Ball one: pos = (%.2f,%.2f) vel = (0,0) acc = (0,0) </p>" %(stillBall.obj.still_ball.pos.x, stillBall.obj.still_ball.pos.y)
            html_content+= "<p> Ball two: pos = (%.2f,%.2f) vel = (%.2f,%.2f) acc = (%.2f,%.2f) </p>" %(rollingBall.obj.rolling_ball.pos.x, rollingBall.obj.rolling_ball.pos.y, rollingBall.obj.rolling_ball.vel.x, rollingBall.obj.rolling_ball.vel.y, rollingBall.obj.rolling_ball.acc.x, rollingBall.obj.rolling_ball.acc.y)
            
            count = 0
            for count in range(x):
                html_content+="""<img src="/table-%d.svg">""" %(count)
                count+=1
            html_content+="""</body>
                        </html>
            """

            content = html_content        

            # Generate the headers
            self.send_response(200)  # OK
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(html_content))
            self.end_headers()

            # Send it to the browser
            self.wfile.write(bytes(html_content, "utf-8"))
            #fp.close()

        else:
            # Generate  404 for PUT requests that aren't the file above
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: %s not found" % self.path, "utf-8"))

if __name__ == "__main__":
    httpd = HTTPServer(('localhost', int(sys.argv[1])), MyHandler)
    print("Server listening in port: ", int(sys.argv[1]))
    httpd.serve_forever()
