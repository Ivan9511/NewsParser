class Source:
    def __init__(self, id: int, name: str, url: str, config: dict):
        self.id = id
        self.name = name
        self.url = url
        self.config = config

        # Извлечение данных из config
        self.rule = config.get("rule")
        self.next_page_rule = config.get("next_page_rule")
        self.title = config.get("title")
        self.contente = config.get("content")
        self.datee = config.get("date")

    def __repr__(self):
        return (
            f"Source(id={self.id}, name='{self.name}', url='{self.url}', "
            f"rule='{self.rule}', next_page_rule='{self.next_page_rule}', "
            f"title='{self.title_rule}', content='{self.content_rule}', "
            f"date='{self.date_rule}')"
        )