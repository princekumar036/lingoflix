
// MOVIES
currentPage = 1
totalPages = 1

function addMovies(currentPage) {
    url_movie = `https://api.themoviedb.org/3/discover/movie?` + 
            `api_key=${'daa7c37e8875b873c494c4070f234516'}` +
            `&page=${currentPage}` +
            `&region=${session['watch_region']}` + 
            `&with_original_language=${session['target_language']}` + 
            `&with_watch_monetization_types=flatrate|free|ads|rent|buy`

    fetch(url_movie)
    .then((response) => response.json())
    .then((data) => {
        totalPages = data['total_pages']
        data.results.forEach(movie => {
            newMovie = `<a href="/movie-details?id=${movie['id']}" class="hover:scale-105 ease-in-out duration-300">
                            <img class="rounded-t h-72 w-full object-cover" src="https://image.tmdb.org/t/p/w500/${movie['poster_path']}" alt="${movie['title']}">
                            <p>${movie['title']} <span class="text-sm opacity-80">(${movie['release_date'].split('-')[0]})</span></p>
                        </a>`
            document.getElementById(`section-movie`).innerHTML += newMovie
        })
    })
}

document.getElementById('more-movie').addEventListener('click', () => {
    currentPage += 1
    if (currentPage < totalPages) {
        addMovies(currentPage)
    }
    if (currentPage === totalPages) {
        document.getElementById('more-movie').classList.add('hidden')
    }
})

addMovies(1)