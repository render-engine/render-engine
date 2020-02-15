# Header Links
class Link:
    def __init__(self, name, url="", image="", links=[]):
        self.name = name
        self.url = url
        self.links = links
        self.image = image

    def __repr__(self):
        return f'{self.name} <{self.url}>'
