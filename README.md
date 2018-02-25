# MovieLens Stream Service Search

This repo allows you to cross-reference queries against a MovieLens account to 
identify which streaming services are available for a returned list of movies. 

This repo is WIP - all functionality is present but still requires testing and user-friendly tidying of the code.

## Setup

- Clone the repository
- Rename the file `config.ini.dist` to `config.ini`
- Add your MovieLens username and password to the `config.ini` file

## Usage

Construct a MovieLens search query - for example, to return a list of your most-recommended, unseen, action movies:

```
{
    'hasRated': 'no',
    'sortBy': 'recommended',
    'genre': 'action'
}
```

Submit this as input to `return_top_list()`; default output will be a JSON of your most recommended movies and links to available streaming services, as below. Default filter excludes providers offering the movies to purchase or rent.

```
[
    {
        "id": 254320,
        "title": "The Lobster",
        "genres": [
            "Thriller",
            "Comedy",
            "Drama",
            "Romance",
            "Science Fiction"
        ],
        "avgRating": 3.62519,
        "myRating": 4.5040584927763225,
        "description": "In a dystopian near future, single people, according to the laws of The City, are taken to The Hotel, where they are obliged to find a romantic partner in forty-five days or are transformed into beasts and sent off into The Woods.",
        "sources": [
            {
                "service": "All4",
                "url": "http://www.channel4.com/programmes/the-lobster/on-demand/59207-001"
            }
        ]
    },
    {
        "id": 334541,
        "title": "Manchester by the Sea",
        "genres": [
            "Drama"
        ],
        "avgRating": 3.84024,
        "myRating": 4.367815804983475,
        "description": "After his older brother passes away, Lee Chandler is forced to return home to care for his 16-year-old nephew. There he is compelled to deal with a tragic past that separated him from his family and the community where he was born and raised.",
        "sources": [
            {
                "service": "Amazon Prime",
                "url": "https://www.amazon.co.uk/gp/product/B01MUCLXZK?camp=1634&creativeASIN=B01MUCLXZK&ie=UTF8&linkCode=xm2&tag=just016-21"
            }
        ]
    }
]
```

I've manually mapped a bunch of the (UK) JustWatch provider IDs to streaming service names; these may not stay static and will evolve as their service evolves so be warned! This can also be used to e.g. filter streaming services you don't have access to. The list is in `providers.json`.

## Credits

This repo makes use of the JustWatch API for Python: https://github.com/dawoudt/JustWatchAPI

The MovieLens requests API is a (very crude) port of the Node.js MovieLens API: https://github.com/pjobson/node-movielens/
