class TitleNotFoundError(Exception):
    def __init__(self, title):
        super().__init__(self)
        self.title = title
        self.message = "Title not found !"
        
    def __str__(self):
        return f"{self.title} : {self.message}"


class EmptyInputError(Exception):
    def __init__(self):
        super().__init__(self)
        self.message = "Remember...All I'm Offering Is The Truth. Nothing More."
    
    def __str__(self):
        return self.message


class PosterError(Exception):
    def __init__(self, title):
        super().__init__(self)
        self.message = f"Poster not available for {title}"
    
    def __str__(self):
        return self.message


class ActorPictureError(Exception):
    def __init__(self, actor):
        super().__init__(self)
        self.message = f"Picture not available for {actor}"
    
    def __str__(self):
        return self.message