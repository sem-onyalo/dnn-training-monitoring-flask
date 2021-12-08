class Config:
    debug:bool
    host:str
    port:str

    def __init__(self) -> None:
        # TODO: read from env vars
        self.debug = True
        self.host = "0.0.0.0"
        self.port = "8080"