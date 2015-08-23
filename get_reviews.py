from requests import session
from bs4 import BeautifulSoup


# this class gets you reviews in a list dictionary format from your Freeindex.co.uk profile so that you can link it
# into your website for testimonials and ect.
class FreeIndexReviews:

    def __init__(self, uri):

        self.uri = uri

        # initializing the session
        s = session()
        self.request = s.get(uri)

        # initializing the list where your reviews will be stored
        self._reviews_list_dict = []

        # getting the html object from the uri provided
        html_soup_obj = BeautifulSoup(self.request.content)

        # checking to make sure there is at least one review
        if len(html_soup_obj.findAll('div', {'class': 'row review'})) > 0:

            # getting the reviews from the html object
            reviews = html_soup_obj.findAll('div', {'class': 'row review'})

            # sorting and finding all reviews in the reviews html and appending it to _reviews_list_dict
            for review in reviews:
                review = BeautifulSoup(str(review))

                self._reviews_list_dict.append(
                    {
                        'rating': float(
                            review.find(
                                'div',
                                {'class': 'ratinglarge '}
                            )['title'][-3:]
                        ),
                        'author': str(
                            review.find(
                                'div',
                                {'itemprop': 'author'}
                            ).text
                        ),
                        'date': str(
                            review.find(
                                'div',
                                {'class': 'summary_rating clearfix pull-left'}
                            ).find(
                                'div',
                                {'class': 'pull-left grey small'}
                            ).text
                        ),
                        'review': ' '.join(
                            review.find(
                                'div',
                                {'itemprop': 'description'}
                            ).findAll(
                                text=True, recursive=False
                            )
                        ),
                        'uri': self.uri
                    }
                )
        else:
            self._reviews_list_dict = [
                {
                    'rating': 0.0,
                    'author': '',
                    'date': '',
                    'review': '',
                    'uri': self.uri
                }
            ]

    # this method, when called, will return your top five reviews based on their rating
    def top_five_reviews(self):
        return list(
            reversed(
                sorted(
                    self._reviews_list_dict,
                    key=lambda review: review['rating']
                )
            )
        )[:5]
