def GetCreateTableCommands():
    commands = []
    
    commands.append(""" DataSources (
                        DataSourceId	INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name	TEXT NOT NULL,
                        Description	BLOB,
                        Color	TEXT,
                        IsActive	INTEGER DEFAULT 1
                    ); """)
    
    commands.append(""" DataSourceTuples (
                        DataSourceTupleId	INTEGER PRIMARY KEY AUTOINCREMENT,
                        DataFilePath	TEXT NOT NULL,
                        ControlDataFilePath	TEXT,
                        DataSourceId	INTEGER NOT NULL,
                        FOREIGN KEY (DataSourceId) REFERENCES DataSources(DataSourceId)
                        ); """)
                        

    
    for i in range(len(commands)):
        commands[i] = " CREATE TABLE IF NOT EXISTS " + commands[i]
        
    return commands
    