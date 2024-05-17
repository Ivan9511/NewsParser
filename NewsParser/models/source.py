class Source:
    def __init__(self, id: int, name: str, url: str, config: dict):
        self.id = id
        self.name = name
        self.url = url
        self.config = config

        # Извлечение данных из config
        self.rule = config.get("rule")
        self.next_page_rule = config.get("next_page_rule")
        self.title_rule = config.get("title")
        self.content_rule = config.get("content")
        self.date_rule = config.get("date")

    def __repr__(self):
        return (
            f"Source(id={self.id}, name='{self.name}', url='{self.url}', "
            f"rule='{self.rule}', next_page_rule='{self.next_page_rule}', "
            f"title_rule='{self.title_rule}', content_rule='{self.content_rule}', "
            f"date_rule='{self.date_rule}')"
        )