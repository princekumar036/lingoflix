
// MOVIES
let movie_pageNo_el = document.getElementById('movie-pageNo')
let movie_pageNo = parseInt(movie_pageNo_el.value)
let movie_form = document.getElementById('movie-form')

movie_form.addEventListener('submit', function(e) {
    e.preventDefault()

    movie_pageNo += 1
    if (movie_pageNo === total_pages) {
        movie_form.classList.add('hidden')
        return
    }
    movie_pageNo_el.setAttribute('value', movie_pageNo)
    const formData = new FormData(movie_form)

    fetch('/movie', {
        method: 'POST',
        body: formData,
    })
    .then((response) => response.json())
    .then((data) => {
        data.forEach(movie => {
            newMovie = `<a href="/movie-details?id=${movie['id']}" class="hover:scale-105 ease-in-out duration-300">
                            <img class="rounded-t h-72 w-full object-cover" src="https://image.tmdb.org/t/p/w185${movie['poster_path']}" alt="${movie['title']}">
                            <p>${movie['title']} <span class="text-sm opacity-80">(${movie['release_date'].split('-')[0]})</span></p>
                        </a>`
            document.getElementById('movie-section').innerHTML += newMovie
        })
    })
})