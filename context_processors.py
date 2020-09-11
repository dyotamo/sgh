def pagination_processor():
    def has_next(pagination):
        return pagination.get_page() < pagination.get_page_count()

    def has_previous(pagination):
        return pagination.get_page() > 1

    def next_page(pagination):
        return pagination.get_page()+1

    def previous_page(pagination):
        return pagination.get_page()-1

    return dict(has_next=has_next, has_previous=has_previous,
                next_page=next_page, previous_page=previous_page)
