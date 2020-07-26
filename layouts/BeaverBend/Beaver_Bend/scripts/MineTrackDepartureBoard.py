import jmri


class MineTrackDepartureBoard(jmri.jmrit.automat.AbstractAutomaton) :

    keepGoing = True

    def init (self) :

        import foggyhollow
        import foggyhollow.departureboard.DepartureBoard

        #global mine_track_departure_board 

        self.keepGoing = True

        #try :
        #    mine_track_departure_board.addField("Train", 0, 3, True)
        #    self.keepGoing = False
            
        #except :
        self.departureBoard = foggyhollow.departureboard.DepartureBoard("Ace of Spades Mine", "Departures", 30, 322, 4, 44)

        print "Done creating departure board"
        self.departureBoard.addField("Train", 0, 3, True)
        self.departureBoard.addField("Direction", 4,1, False)		                
        self.departureBoard.addField("Destination", 6, 23, False)		
        self.departureBoard.addField("Departs", 30, 5, True)
        self.departureBoard.addField("Status", 36, 8, True)			
        self.departureBoard.addField("LocoDescr", 0, 44, False)

        self.departureBoard.clearRow(0, False)
        self.departureBoard.clearRow(1, False)
        self.departureBoard.clearRow(2, False)
        self.departureBoard.clearRow(3, True)        

        self.departureBoard.setField("LocoDescr", "Welcome to the", 1, 0)
        self.departureBoard.setField("LocoDescr", "Foggy Hollow & Western RailRoad", 2, 0)	
        self.departureBoard.setField("LocoDescr", "Beaver Bend Division", 3, 0)

        storedDepBoard = memories.provide("Departure Board");
        storedDepBoard.setUserName("Departure Board")
        storedDepBoard.setValue(self.departureBoard)
        
    def handle(self):
        self.waitMsec (60000)
        return self.keepGoing

mtdb = MineTrackDepartureBoard()
mtdb.setName("Mine Track Departure Board")
mtdb.start()
