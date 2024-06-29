import phylib
import os
import sqlite3
# add stuff here
HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";
FOOTER = """</svg>\n"""

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS  = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;
DRAG = phylib.PHYLIB_DRAG;
MAX_TIME = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;
# Assignment 3 starts
FRAME_INTERVAL = 0.01


# add more here

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here

    def svg(self):
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" %(self.obj.still_ball.pos.x,self.obj.still_ball.pos.y,BALL_RADIUS,BALL_COLOURS[self.obj.still_ball.number])

class RollingBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos, vel, acc, ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = RollingBall;


    # add an svg method here
    def svg(self):
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" %(self.obj.rolling_ball.pos.x,self.obj.rolling_ball.pos.y,BALL_RADIUS,BALL_COLOURS[self.obj.rolling_ball.number])

class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self,pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       0, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = Hole;


    # add an svg method here
    def svg(self):
       return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" %(self.obj.hole.pos.x, self.obj.hole.pos.y,HOLE_RADIUS)


class VCushion( phylib.phylib_object ):
    """
    Python Vcushion class.
    """

    def __init__( self,x ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       0, 
                                       None, None, None, 
                                       x,0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = VCushion;


    # add an svg method here
    def svg(self):
        numValue = 0
        if self.obj.vcushion.x == 0:
            numValue = -25
        else:
            numValue = 2700
        return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (numValue)

class HCushion( phylib.phylib_object ):
    """
    Python Hcushion class.
    """

    def __init__( self,y ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       0, 
                                       None, None, None, 
                                       0.0, y );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = HCushion;
    
    def svg(self):
        valueNum = 0
        if self.obj.hcushion.y == 0:
            valueNum = -25
        else:
            valueNum = 1350
        return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (
            valueNum
        )


class Table(phylib.phylib_table):
    """
    Pool table class.
    """

    def __init__(self):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__(self)
        self.current = -1

    def __iadd__(self, other):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object(other)
        return self

    def __iter__(self):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self

    def __next__(self):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1  # increment the index to the next object
        if self.current < MAX_OBJECTS:  # check if there are no more objects
            return self[self.current]  # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1  # reset the index counter
        raise StopIteration  # raise StopIteration to tell for loop to stop

    def __getitem__(self, index):
        """
        This method adds item retrieval support using square brackets [ ].
        It calls get_object (see phylib.i) to retrieve a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object(index)
        if result == None:
            return None
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion
        return result

    def __str__(self):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = ""  # create empty string
        result += "time = %6.1f;\n" % self.time  # append time
        for i, obj in enumerate(self):  # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i, obj)  # append object description
        return result  # return the string

    def segment(self):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """
        result = phylib.phylib_table.segment(self)
        if result:
            result.__class__ = Table
            result.current = -1
        return result

    # add svg method here

    def svg(self):
        nameString = HEADER
        for obj in self:
            if obj != None:
                nameString += obj.svg()
        nameString += FOOTER
        return nameString
    
    def roll(self, t):
        new = Table()
        for ball in self:
            if isinstance(ball, RollingBall):
                # create a new ball with the same number as the old ball
                new_ball = RollingBall(ball.obj.rolling_ball.number,
                                    Coordinate(0, 0),
                                    Coordinate(0, 0),
                                    Coordinate(0, 0))
                # compute where it rolls to
                phylib.phylib_roll(new_ball, ball, t)
                # add ball to table
                new += new_ball
            if isinstance(ball, StillBall):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall(ball.obj.still_ball.number,
                                    Coordinate(ball.obj.still_ball.pos.x,
                                                ball.obj.still_ball.pos.y))
                # add ball to table
                new += new_ball
        # return table
        return new
    
        
    def cueBall(self):
        for ball in self:
            if isinstance(ball, StillBall) and ball.obj.still_ball.number == 0:
                cueBall = ball
        return cueBall 
        

class Database:
    def __init__(self, reset=False):
        if reset:
            if os.path.exists("phylib.db"):
                os.remove("phylib.db")

        # Connect to the database
        self.conn = sqlite3.connect("phylib.db")
        self.cursor = self.conn.cursor()

        # Create a table if it does not already exist

        self.conn.commit()

    def createDB(self):
        cur = self.conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS Ball
                         (BALLID    INTEGER NOT NULL,
                          BALLNO    INTEGER NOT NULL,
                          XPOS      FLOAT   NOT NULL,
                          YPOS      FLOAT   NOT NULL,
                          XVEL      FLOAT,
                          YVEL      FLOAT,
                          PRIMARY KEY (BALLID AUTOINCREMENT) );""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS TTable
                         (TABLEID   INTEGER NOT NULL,
                          TIME      FLOAT   NOT NULL,
                          PRIMARY KEY (TABLEID AUTOINCREMENT) );""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS BallTable
                         (
                          BALLID    INTEGER NOT NULL,
                          TABLEID   INTEGER NOT NULL,
                         
                          FOREIGN KEY (BALLID) REFERENCES Ball
                          FOREIGN KEY (TABLEID) REFERENCES TTable )""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS Shot
                         (SHOTID    INTEGER NOT NULL,
                          PLAYERID  INTEGER NOT NULL,
                          GAMEID    INTEGER NOT NULL,
                          PRIMARY KEY (SHOTID AUTOINCREMENT)
                          FOREIGN KEY (GAMEID) REFERENCES Game 
                          FOREIGN KEY (PLAYERID) REFERENCES Player )""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS TableShot
                        (TABLEID    INTEGER NOT NULL,
                         SHOTID     INTEGER NOT NULL,
                         FOREIGN KEY (TABLEID) REFERENCES TTable
                         FOREIGN KEY (SHOTID) REFERENCES Shot)""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS Game
                        ( GAMEID     INTEGER NOT NULL,
                         GAMENAME   VARCHAR(64) NOT NULL,
                         PRIMARY KEY(GAMEID AUTOINCREMENT))""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS Player
                         (PLAYERID   INTEGER NOT NULL,
                         GAMEID     INTEGER NOT NULL,
                         PLAYERNAME VARCHAR(64) NOT NULL,
                         PRIMARY KEY (PLAYERID AUTOINCREMENT)
                         FOREIGN KEY (GAMEID) REFERENCES Game) """)
        
        self.conn.commit()
        cur.close()

        
    def readTable(self, tableID):
        # defining table here
        returnTable = Table()
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM BallTable WHERE TABLEID = ?", (tableID + 1, ))
        selectID = cursor.fetchone()[0]

        if selectID == 0:
            cursor.close()
            return None
        
        cursor.execute("SELECT Ball.BALLID,Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL FROM Ball JOIN BallTable ON Ball.BALLID = BallTable.BALLID WHERE BallTable.TABLEID = ?", (tableID+1, ))
        dataBall = cursor.fetchall()
        

        for ball in dataBall:
            if ball[4] == None and ball[5] == None:
                positionCoordinate = Coordinate(ball[2], ball[3])
                newBall = StillBall(ball[1], positionCoordinate)
                returnTable += newBall
            else:
                velocityCoordinate = Coordinate(ball[4], ball[5])
                positionCoordinate = Coordinate(ball[2], ball[3])

                accelerationValue = Coordinate(0.0,  0.0)
                speed = phylib.phylib_length(velocityCoordinate)

                accelerationValue_x = 0.0
                accelerationValue_y = 0.0
            
                if speed > VEL_EPSILON:
                    accelerationValue_x = -ball[4] / speed * DRAG
                    accelerationValue_y = -ball[5] / speed * DRAG
                accelerationCoordinate = Coordinate(accelerationValue_x, accelerationValue_y)
                newBall = RollingBall(ball[1], positionCoordinate, velocityCoordinate, accelerationCoordinate)
                returnTable += newBall

        
        cursor.execute("SELECT TIME FROM TTable WHERE TABLEID = ?", (tableID+1, ))
        storeTime = cursor.fetchone()[0]
        returnTable.time = storeTime


        self.conn.commit()
        cursor.close()
        return returnTable


    def writeTable(self, table):
        cur = self.conn.cursor()

        cur.execute("INSERT INTO TTable (TIME) VALUES (?)", (table.time,))
        table_id = cur.lastrowid  

        for obj in table:
            # if isinstance(obj, (StillBall, RollingBall)):
            if isinstance(obj, StillBall):
                    # For still balls, insert with XVEL and YVEL velocities as 0
                    cur.execute("INSERT INTO Ball (BALLNO, XPOS, YPOS) VALUES (?, ?, ?)",
                                        (obj.obj.still_ball.number, obj.obj.still_ball.pos.x, obj.obj.still_ball.pos.y,))
            elif isinstance(obj, RollingBall):
                    cur.execute("INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?)",
                                        (obj.obj.rolling_ball.number, obj.obj.rolling_ball.pos.x, obj.obj.rolling_ball.pos.y,
                                         obj.obj.rolling_ball.vel.x, obj.obj.rolling_ball.vel.y,))
            else:
                continue

            ball_id = cur.lastrowid
            # Map ball to the table in BallTable
            cur.execute("INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)", (ball_id, table_id))
            
        cur.connection.commit()
        cur.close()

        return table_id - 1
 
    
    def newShot(self, gameID, playerID):
        try:
            self.cursor.execute("INSERT INTO Shot (gameID, playerID) VALUES (?, ?)", (gameID, playerID))
            shotID = self.cursor.lastrowid
            self.conn.commit()
            return shotID
        finally:
        # Close the cursor
            self.cursor.close()
            self.conn.commit()
        # Close the connection
            #self.connection.close()

    def insertTableShot(self,tableID, shotID):
        cursor = self.conn.cursor()


        cursor.execute("""INSERT
                       INTO TableShot (TABLEID, SHOTID)
                       VALUES (?,?)""", (tableID, shotID))
        
        self.conn.commit()
        cursor.close()


    def close(self):
        self.conn.commit()
        self.conn.close()

    def getConnection(self):
        return self.conn


class Game:
    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        self.db = Database()
        self.db.createDB()
        self.Connection = self.db.getConnection()

        startGame = 0

        if isinstance(gameID, int) and gameName is None and player1Name is None and player2Name is None:
            startGame = 1
        elif gameID is None and isinstance(gameName,str) and isinstance(player1Name,str) and isinstance(player2Name,str):
            startGame = 2
        else:
            startGame = 0
        
        if startGame == 0:
            raise TypeError("This is an invalid argument")
        
        cursor = self.Connection.cursor()

        if startGame == 1:
            

            cursor.execute("""
                           SELECT Game.GAMENAME, Player.PLAYERNAME
                           FROM GAME
                           JOIN Player ON Game.GAMEID = Player.GAMEID
                           WHERE Game.GameID = ?;
                           """,(gameID + 1,))
            
            gamelogic = cursor.fetchall()
            if not gamelogic:
                self.gameName = gameName
                self.player1Name = player1Name
                self.player2Name = player2Name

        if startGame == 2:
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name

            cursor.execute("""
                           INSERT
                           INTO Game (GAMENAME)
                        VALUES    (?);
                           """,(self.gameName,))
            
            cursor.execute("""
                           SELECT Game.GAMEID
                           FROM Game 
                           WHERE Game.GAMENAME = ?;
                           """,(self.gameName,))
            
            gameID = cursor.fetchall()[0][0]
            self.gameID = gameID - 1

            cursor.execute("""
                           INSERT
                           INTO Player (PLAYERNAME, GAMEID)
                           VALUES       (?,?)
                           """,(self.player1Name,gameID))

            cursor.execute("""
                           INSERT
                           INTO Player (PLAYERNAME, GAMEID)
                           VALUES       (?,?)
                           """,(self.player2Name,gameID))

            self.db.close()

    def shoot(self, gameName,playerName,table, xvel, yvel):
        

        self.db = Database();


        shotID = self.db.newShot(gameName, playerName)
        ballCue = table.cueBall()

        if ballCue is not None:
            xpos = ballCue.obj.still_ball.pos.x
            ypos = ballCue.obj.still_ball.pos.y

            ballCue.type = phylib.PHYLIB_ROLLING_BALL
            ballCue.obj.rolling_ball.number = 0
            ballCue.obj.rolling_ball.pos.x = xpos
            ballCue.obj.rolling_ball.pos.y = ypos
            ballCue.obj.rolling_ball.vel.x = xvel
            ballCue.obj.rolling_ball.vel.y = yvel

            ballSpeed = phylib.phylib_length(ballCue.obj.rolling_ball.vel)

            if  ballSpeed > VEL_EPSILON:
                ballCue.obj.rolling_ball.acc.x = -ballCue.obj.rolling_ball.vel.x / ballSpeed * DRAG
                ballCue.obj.rolling_ball.acc.y = -ballCue.obj.rolling_ball.vel.y / ballSpeed * DRAG

            while table:
                timeStart = table.time
                copy = table
                table = table.segment()

                if table is not None:
                    timeEnd = table.time

                timeFinal = timeEnd - timeStart
                timeFinal = int(timeFinal // FRAME_INTERVAL)

                for frame in range(timeFinal):
                    tableUpdate = copy.roll(frame * FRAME_INTERVAL)
                    tableUpdate.time = timeStart + (frame * FRAME_INTERVAL)
                    tableID = self.db.writeTable(tableUpdate)
                    self.db.insertTableShot(tableID, shotID)

        self.db.close()
